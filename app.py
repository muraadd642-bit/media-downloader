import streamlit as st
import yt_dlp
import os
import datetime
import random

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SSSMurad - Ultra Downloader",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── MOTIVASIYA CÜMLƏLƏRİ ────────────────────────────────────────────────────
MOTIVATIONS = [
    "⚡ Hər sınaq sənin gizli gücünü ortaya çıxarır. Bu gün bir addım at!",
    "🔥 Uğur heç vaxt təsadüf deyil - o, planın nəticəsidir.",
    "🚀 İmtahan sonu deyil, yeni başlanğıcın qapısıdır.",
    "💡 Bilik silah, səbr isə qalxandır. İkisini də siyir!",
    "💪 Sınaq sənə layiq deyil - SƏN SINAĞA LAYİQSƏN!",
]

# ─── USER-AGENT ROTASIYASI ────────────────────────────────────────────────────
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]

def get_random_ua():
    return random.choice(USER_AGENTS)

def get_headers(url: str) -> dict:
    referer = "https://www.instagram.com/" if "instagram" in url else \
              "https://www.tiktok.com/"    if "tiktok" in url    else \
              "https://www.youtube.com/"
    return {
        "User-Agent": get_random_ua(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,az;q=0.8",
        "Referer": referer,
        "DNT": "1",
    }

# ─── COOKIES YOXLAMA ─────────────────────────────────────────────────────────
COOKIE_FILE = "cookies.txt"

def cookies_available() -> bool:
    return os.path.isfile(COOKIE_FILE) and os.path.getsize(COOKIE_FILE) > 0

# ─── YDL OPTS BUILDER ────────────────────────────────────────────────────────
def build_ydl_opts(url: str, fmt: str, quality: str, output_path: str) -> dict:
    ua = get_random_ua()
    headers = get_headers(url)

    if fmt == "MP3":
        format_sel = "bestaudio/best"
        postprocessors = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    else:
        # TikTok və IG üçün daha stabil format filtri
        q_map = {
            "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
            "720p":  "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best",
            "480p":  "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best"
        }
        format_sel = q_map.get(quality, "bestvideo+bestaudio/best")
        postprocessors = [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}]

    opts = {
        "format": format_sel,
        "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
        "postprocessors": postprocessors,
        "http_headers": headers,
        "user_agent": ua,
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,
        "socket_timeout": 30,
        "noplaylist": True,
        "extract_flat": False,
        "merge_output_format": "mp4" if fmt == "MP4" else None,
        "extractor_args": {
            "tiktok": {"web_api": True},
            "instagram": {"get_video_id": ["web_api"]}
        }
    }

    if cookies_available():
        opts["cookiefile"] = COOKIE_FILE

    return opts

# ─── DOWNLOADER ───────────────────────────────────────────────────────────────
def download_media(url: str, fmt: str, quality: str) -> tuple[bool, str, str | None]:
    output_dir = "/tmp/sssmurad_downloads"
    os.makedirs(output_dir, exist_ok=True)
    opts = build_ydl_opts(url, fmt, quality, output_dir)

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "media")
            ext = "mp3" if fmt == "MP3" else "mp4"
            for f in os.listdir(output_dir):
                if f.endswith(f".{ext}"):
                    return True, f"✅ '{title}' hazırdır!", os.path.join(output_dir, f)
            return True, "✅ Yükləndi.", None
    except Exception as e:
        return False, f"❌ Xəta: {str(e)[:50]}...", None

# ─── CSS (Claude's Style) ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Rajdhani:wght@400;600&display=swap');
:root { --neon-blue: #00d4ff; --bg-deep: #020817; --bg-card: rgba(0, 20, 50, 0.55); }
html, body, [data-testid="stAppViewContainer"] { background: var(--bg-deep) !important; font-family: 'Rajdhani', sans-serif !important; color: #e2f4ff !important; }
.glass-card { background: var(--bg-card); border: 1px solid rgba(0, 212, 255, 0.35); border-radius: 18px; padding: 2rem; backdrop-filter: blur(18px); margin-bottom: 1.5rem; }
.murad-title { font-family: 'Orbitron', monospace !important; font-size: 2.6rem; text-align: center; background: linear-gradient(135deg, #00d4ff 0%, #ff2d78 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.stButton>button { background: linear-gradient(135deg, #003d5c, #001a35) !important; border: 1px solid var(--neon-blue) !important; color: var(--neon-blue) !important; font-family: 'Orbitron' !important; width: 100%; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p style="font-family:\'Orbitron\'; color:#00d4ff; text-align:center;">⚡ MURAD AI PRO</p>', unsafe_allow_html=True)
    days_left = (datetime.date(2026, 6, 7) - datetime.date.today()).days
    st.info(f"🎯 Blok İmtahanına: {days_left} Gün")
    st.write(f"🍪 Cookie: {'✅ Aktiv' if cookies_available() else '✗ Yoxdur'}")

# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────
st.markdown('<div class="murad-title">⚡ SSSMurad</div>', unsafe_allow_html=True)
if "motivation" not in st.session_state: st.session_state.motivation = random.choice(MOTIVATIONS)
st.success(st.session_state.motivation)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
url = st.text_input("🔗 Media URL:", placeholder="Link bura yapışdırın...")
fmt = st.radio("📦 Format:", ["MP4 (Video)", "MP3 (Musiqi)"], horizontal=True)
quality = st.selectbox("🎚️ Keyfiyyət:", ["1080p", "720p", "480p"]) if "Video" in fmt else "best"
human = st.checkbox("✅ Mən robot deyiləm")
st.markdown('</div>', unsafe_allow_html=True)

if st.button("⬇ YÜKLƏ", disabled=not (url and human)):
    success, msg, filepath = download_media(url.strip(), "MP4" if "Video" in fmt else "MP3", quality)
    if success and filepath:
        st.toast(msg)
        with open(filepath, "rb") as f:
            st.download_button("💾 Faylı Saxla", f, file_name=os.path.basename(filepath))
        os.remove(filepath)
    else: st.error(msg)
