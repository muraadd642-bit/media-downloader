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
    "🎯 Hər sual bir imkandır. Qaçma, çöz!",
    "🏆 Şampionlar yorulmur - yalnız zəiflər əvvəlcədən təslim olur.",
    "💪 Sınaq sənə layiq deyil - SƏN SINAĞA LAYİQSƏN!",
    "🦅 Yüksəl, çünki zirvə sənin yerindir.",
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
        "Sec-Fetch-Mode": "navigate",
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
        # TIKTOK ÜÇÜN DÜZƏLDİLMİŞ FORMAT SEÇİMİ
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
        return False, f"❌ Xəta baş verdi. Linki yoxlayın.", None

# ─── CSS (FULL CLAUDE DESIGN) ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

:root {
    --neon-blue:   #00d4ff;
    --neon-pink:   #ff2d78;
    --neon-green:  #00ff9d;
    --bg-deep:     #020817;
    --bg-card:     rgba(0, 20, 50, 0.55);
    --border-glow: rgba(0, 212, 255, 0.35);
    --text-main:   #e2f4ff;
    --text-muted:  #7ab3cc;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-deep) !important;
    font-family: 'Rajdhani', sans-serif !important;
    color: var(--text-main) !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background: 
        radial-gradient(ellipse at 20% 50%, rgba(0,212,255,0.06) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(255,45,120,0.05) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

.murad-header { text-align: center; padding: 2rem 0; }
.murad-title {
    font-family: 'Orbitron', monospace !important;
    font-size: 2.6rem;
    font-weight: 900;
    background: linear-gradient(135deg, var(--neon-blue) 0%, var(--neon-pink) 50%, var(--neon-green) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 2px;
}

.glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border-glow);
    border-radius: 18px;
    padding: 2rem;
    backdrop-filter: blur(18px);
    box-shadow: 0 0 40px rgba(0,212,255,0.08);
    margin-bottom: 1.5rem;
    position: relative;
}

.section-label {
    font-family: 'Orbitron', monospace;
    font-size: 0.72rem;
    color: var(--neon-blue);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

.stButton > button {
    background: linear-gradient(135deg, #003d5c, #001a35) !important;
    border: 1px solid var(--neon-blue) !important;
    color: var(--neon-blue) !important;
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 2px !important;
    border-radius: 10px !important;
    width: 100% !important;
    padding: 0.7rem !important;
}

.stButton > button:hover {
    box-shadow: 0 0 30px rgba(0,212,255,0.4) !important;
    color: #fff !important;
}

/* Countdown Style */
.countdown-container {
    background: rgba(0,212,255,0.06);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
}
.countdown-num { font-family: 'Orbitron'; font-size: 1.8rem; font-weight: 900; color: #fff; }

</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p style="font-family:\'Orbitron\'; font-size:1rem; color:#00d4ff; text-align:center;">⚡ MURAD AI PRO</p>', unsafe_allow_html=True)
    
    # Geri sayım
    target = datetime.date(2026, 6, 7)
    days_left = (target - datetime.date.today()).days
    st.markdown(f"""
    <div class="countdown-container">
        <div style="font-size:0.7rem; color:#00d4ff; letter-spacing:2px;">🎯 İMTAHANA QALDI</div>
        <div class="countdown-num">{max(days_left, 0)}</div>
        <div style="font-size:0.6rem; color:#7ab3cc;">GÜN</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    cookie_status = "✅ Aktiv" if cookies_available() else "✗ Yoxdur"
    st.info(f"🍪 Cookie Statusu: {cookie_status}")

# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────
st.markdown("""<div class="murad-header"><div class="murad-title">⚡ SSSMurad</div></div>""", unsafe_allow_html=True)

if "motivation" not in st.session_state: st.session_state.motivation = random.choice(MOTIVATIONS)
st.markdown(f'<div style="background:rgba(0,212,255,0.08); border:1px solid rgba(0,212,255,0.2); border-radius:12px; padding:1rem; text-align:center; color:#00d4ff; margin-bottom:1.5rem;">{st.session_state.motivation}</div>', unsafe_allow_html=True)

# URL və Format Kartı
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">🔗 MEDIA URL</div>', unsafe_allow_html=True)
url = st.text_input("", placeholder="Link bura...", label_visibility="collapsed")

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="section-label">📦 FORMAT</div>', unsafe_allow_html=True)
    fmt = st.radio("", ["MP4 (Video)", "MP3 (Musiqi)"], label_visibility="collapsed")
with col2:
    st.markdown('<div class="section-label">🎚️ KEYFİYYƏT</div>', unsafe_allow_html=True)
    quality = st.selectbox("", ["1080p", "720p", "480p"], label_visibility="collapsed") if "Video" in fmt else "best"
st.markdown('</div>', unsafe_allow_html=True)

# Robot Check
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">🔐 TƏHLÜKƏSİZLİK</div>', unsafe_allow_html=True)
human = st.checkbox("✅ Mən robot deyiləm — yükləməni təsdiqləyirəm")
st.markdown('</div>', unsafe_allow_html=True)

# Download Button
if st.button("⬇ YÜKLƏ", disabled=not (url and human)):
    with st.spinner("🚀 Murad AI işləyir..."):
        success, msg, filepath = download_media(url.strip(), "MP4" if "Video" in fmt else "MP3", quality)
        if success and filepath:
            st.success(msg)
            with open(filepath, "rb") as f:
                st.download_button("💾 Faylı Saxla", f, file_name=os.path.basename(filepath))
            os.remove(filepath)
        else: st.error(msg)
