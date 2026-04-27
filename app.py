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
    "🌊 Dalğa nə qədər böyük olursa olsun, sən daha güclüsün.",
    "🏆 Şampionlar yorulmur - yalnız zəiflər əvvəlcədən təslim olur.",
    "🌟 Bu an öyrəndiklərin sabahın silahları olacaq.",
    "💪 Sınaq sənə layiq deyil - SƏN SINAĞA LAYİQSƏN!",
    "🦅 Yüksəl, çünki zirvə sənin yerindir.",
]

# ─── USER-AGENT ROTASIYASI ────────────────────────────────────────────────────
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Android 14; Mobile; rv:125.0) Gecko/125.0 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
]

def get_random_ua():
    return random.choice(USER_AGENTS)

def get_headers(url: str) -> dict:
    referer = "https://www.instagram.com/" if "instagram" in url else \
              "https://www.tiktok.com/"    if "tiktok" in url   else \
              "https://www.youtube.com/"
    return {
        "User-Agent": get_random_ua(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,az;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": referer,
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
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
        outtmpl = os.path.join(output_path, "%(title)s.%(ext)s")
    else:
        q_map = {"1080p": "137+140/bestvideo[height<=1080]+bestaudio/best",
                 "720p":  "136+140/bestvideo[height<=720]+bestaudio/best",
                 "480p":  "135+140/bestvideo[height<=480]+bestaudio/best"}
        format_sel = q_map.get(quality, "bestvideo+bestaudio/best")
        postprocessors = [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}]
        outtmpl = os.path.join(output_path, "%(title)s.%(ext)s")

    opts = {
        "format": format_sel,
        "outtmpl": outtmpl,
        "postprocessors": postprocessors,
        "http_headers": headers,
        "user_agent": ua,
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,
        "retries": 5,
        "fragment_retries": 10,
        "socket_timeout": 30,
        "geo_bypass": True,
        "age_limit": None,
        "merge_output_format": "mp4" if fmt == "MP4" else None,
    }

    if cookies_available():
        opts["cookiefile"] = COOKIE_FILE

    return opts

# ─── DOWNLOADER ───────────────────────────────────────────────────────────────
def download_media(url: str, fmt: str, quality: str) -> tuple[bool, str, str | None]:
    """
    Returns (success, message, filepath_or_None)
    """
    output_dir = "/tmp/sssmurad_downloads"
    os.makedirs(output_dir, exist_ok=True)

    opts = build_ydl_opts(url, fmt, quality, output_dir)

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "media")
            ext = "mp3" if fmt == "MP3" else "mp4"
            # find downloaded file
            for f in os.listdir(output_dir):
                if f.endswith(f".{ext}"):
                    return True, f"✅ '{title}' uğurla yükləndi!", os.path.join(output_dir, f)
            return True, f"✅ '{title}' yükləndi.", None
    except yt_dlp.utils.DownloadError as e:
        err = str(e).lower()
        if any(k in err for k in ["login", "private", "sign in", "cookie", "authentication", "403", "rate"]):
            return False, "⚠️ Sistem hal-hazırda məşğuldur. Bir az sonra yenidən yoxlayın.", None
        if "not available" in err or "geo" in err:
            return False, "🌍 Bu məzmun sizin bölgənizdə mövcud deyil.", None
        return False, "❌ Yükləmə uğursuz oldu. URL-i yoxlayın və yenidən cəhd edin.", None
    except Exception:
        return False, "❌ Gözlənilməz xəta. Bir az sonra yenidən cəhd edin.", None

# ─── CSS ──────────────────────────────────────────────────────────────────────
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

/* Animated starfield background */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(0,212,255,0.06) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(255,45,120,0.05) 0%, transparent 50%),
        radial-gradient(ellipse at 60% 80%, rgba(0,255,157,0.04) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* Header */
.murad-header {
    text-align: center;
    padding: 2rem 0 1.5rem;
    position: relative;
}
.murad-title {
    font-family: 'Orbitron', monospace !important;
    font-size: 2.6rem;
    font-weight: 900;
    background: linear-gradient(135deg, var(--neon-blue) 0%, var(--neon-pink) 50%, var(--neon-green) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
    letter-spacing: 2px;
    animation: pulse-title 3s ease-in-out infinite;
}
@keyframes pulse-title {
    0%, 100% { filter: brightness(1); }
    50%       { filter: brightness(1.3); }
}
.murad-sub {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    color: var(--text-muted);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* Glassmorphism card */
.glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border-glow);
    border-radius: 18px;
    padding: 2rem 2.2rem;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    box-shadow:
        0 0 40px rgba(0,212,255,0.08),
        0 8px 32px rgba(0,0,0,0.6),
        inset 0 1px 0 rgba(255,255,255,0.06);
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-blue), var(--neon-pink), transparent);
    animation: scan-line 4s linear infinite;
}
@keyframes scan-line {
    0%   { opacity: 0.4; }
    50%  { opacity: 1;   }
    100% { opacity: 0.4; }
}

/* Motivation banner */
.motivation-banner {
    background: linear-gradient(135deg, rgba(0,212,255,0.08), rgba(255,45,120,0.06));
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 12px;
    padding: 1rem 1.4rem;
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--neon-blue);
    text-align: center;
    letter-spacing: 0.5px;
    margin-bottom: 1.5rem;
}

/* Labels */
.section-label {
    font-family: 'Orbitron', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 3px;
    color: var(--neon-blue);
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

/* Neon input override */
[data-testid="stTextInput"] input {
    background: rgba(0,20,50,0.7) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 10px !important;
    color: var(--text-main) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.7rem 1rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--neon-blue) !important;
    box-shadow: 0 0 12px rgba(0,212,255,0.3) !important;
}

/* Radio buttons */
[data-testid="stRadio"] label {
    color: var(--text-main) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
}

/* Selectbox */
[data-testid="stSelectbox"] div {
    background: rgba(0,20,50,0.7) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 10px !important;
    color: var(--text-main) !important;
}

/* Download button */
.stDownloadButton > button, .stButton > button {
    background: linear-gradient(135deg, #003d5c, #001a35) !important;
    border: 1px solid var(--neon-blue) !important;
    color: var(--neon-blue) !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    border-radius: 10px !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.15) !important;
}
.stDownloadButton > button:hover, .stButton > button:hover {
    background: linear-gradient(135deg, #004d75, #002244) !important;
    box-shadow: 0 0 30px rgba(0,212,255,0.4) !important;
    transform: translateY(-2px) !important;
    color: #fff !important;
}

/* Status boxes */
.status-success {
    background: rgba(0,255,157,0.08);
    border: 1px solid rgba(0,255,157,0.35);
    border-radius: 10px;
    padding: 1rem;
    color: var(--neon-green);
    font-weight: 600;
    text-align: center;
}
.status-error {
    background: rgba(255,45,120,0.08);
    border: 1px solid rgba(255,45,120,0.35);
    border-radius: 10px;
    padding: 1rem;
    color: var(--neon-pink);
    font-weight: 600;
    text-align: center;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(0, 8, 22, 0.95) !important;
    border-right: 1px solid var(--border-glow) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-main) !important;
}

/* Countdown */
.countdown-container {
    background: rgba(0,212,255,0.06);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    margin-top: 1rem;
}
.countdown-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.7rem;
    letter-spacing: 3px;
    color: var(--neon-blue);
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.countdown-num {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 900;
    color: #fff;
    line-height: 1;
}
.countdown-unit {
    font-size: 0.65rem;
    letter-spacing: 2px;
    color: var(--text-muted);
    text-transform: uppercase;
}
.countdown-grid {
    display: flex;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
}
.countdown-cell {
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* Checkbox custom */
.robot-check {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    background: rgba(0,20,50,0.5);
    border: 1px solid var(--border-glow);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin: 0.8rem 0;
    cursor: pointer;
}
.robot-icon { font-size: 1.4rem; }

/* Cookie badge */
.cookie-badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1px;
}
.badge-ok   { background: rgba(0,255,157,0.15); color: var(--neon-green); border: 1px solid rgba(0,255,157,0.3); }
.badge-miss { background: rgba(255,45,120,0.1); color: var(--neon-pink);  border: 1px solid rgba(255,45,120,0.25); }

/* Divider */
.neon-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--neon-blue), transparent);
    margin: 1.5rem 0;
    opacity: 0.4;
}

/* Platform badges */
.platform-badges { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; }
.pbadge {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1px;
}
.pb-yt { background: rgba(255,0,0,0.15);    color: #ff4444; border: 1px solid rgba(255,0,0,0.3); }
.pb-ig { background: rgba(200,60,255,0.12); color: #c83cff; border: 1px solid rgba(200,60,255,0.3); }
.pb-tt { background: rgba(0,212,255,0.12);  color: var(--neon-blue); border: 1px solid var(--border-glow); }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p style="font-family:\'Orbitron\',monospace; font-size:1rem; font-weight:700; color:#00d4ff; letter-spacing:2px; text-align:center;">⚡ MURAD AI PRO</p>', unsafe_allow_html=True)
    st.markdown('<hr style="border:none;height:1px;background:linear-gradient(90deg,transparent,#00d4ff,transparent);opacity:0.3;margin:0.5rem 0 1.5rem;">', unsafe_allow_html=True)

    # Countdown
    target = datetime.date(2026, 6, 7)
    today = datetime.date.today()
    delta = target - today
    days_left = max(delta.days, 0)
    weeks_left = days_left // 7
    remaining_days = days_left % 7

    st.markdown(f"""
    <div class="countdown-container">
        <div class="countdown-title">🎯 İmtahan Geri Sayımı</div>
        <div class="countdown-grid">
            <div class="countdown-cell">
                <span class="countdown-num">{days_left}</span>
                <span class="countdown-unit">Gün</span>
            </div>
            <div class="countdown-cell">
                <span class="countdown-num">{weeks_left}</span>
                <span class="countdown-unit">Həftə</span>
            </div>
            <div class="countdown-cell">
                <span class="countdown-num">{remaining_days}</span>
                <span class="countdown-unit">Artıq</span>
            </div>
        </div>
        <div style="margin-top:0.8rem; font-size:0.78rem; color:#7ab3cc;">
            🗓️ Hədəf: 7 İyun 2026
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr style="border:none;height:1px;background:linear-gradient(90deg,transparent,#00d4ff,transparent);opacity:0.3;margin:1.5rem 0;">', unsafe_allow_html=True)

    # Cookies status
    cookie_status = cookies_available()
    badge_class = "badge-ok" if cookie_status else "badge-miss"
    badge_text = "✓ Aktiv" if cookie_status else "✗ Yoxdur"
    st.markdown(f"""
    <p style="font-family:'Orbitron',monospace; font-size:0.65rem; letter-spacing:2px; color:#7ab3cc; text-transform:uppercase; margin-bottom:0.4rem;">Cookie Statusu</p>
    <span class="cookie-badge {badge_class}">{badge_text}</span>
    """, unsafe_allow_html=True)

    if not cookie_status:
        st.markdown('<p style="font-size:0.78rem; color:#7ab3cc; margin-top:0.5rem;">💡 <code>cookies.txt</code> faylını app.py ilə eyni qovluğa yerləşdir.</p>', unsafe_allow_html=True)

    st.markdown('<hr style="border:none;height:1px;background:linear-gradient(90deg,transparent,#00d4ff,transparent);opacity:0.3;margin:1.5rem 0;">', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:0.78rem; color:#7ab3cc; line-height:1.7;">
        <b style="color:#00d4ff;">Dəstəklənən platformalar:</b><br>
        📺 YouTube &nbsp; 📸 Instagram<br>
        🎵 TikTok &nbsp;&nbsp; 🐦 Twitter/X<br>
        🎬 Vimeo &nbsp;&nbsp;&nbsp; + 1000 sayt
    </div>
    """, unsafe_allow_html=True)

# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────

# Header
st.markdown("""
<div class="murad-header">
    <div class="murad-title">⚡ SSSMurad</div>
    <div class="murad-sub">Ultra Downloader · Pro Edition</div>
</div>
""", unsafe_allow_html=True)

# Motivation (session-stable)
if "motivation" not in st.session_state:
    st.session_state.motivation = random.choice(MOTIVATIONS)

st.markdown(f'<div class="motivation-banner">{st.session_state.motivation}</div>', unsafe_allow_html=True)

# Platform badges
st.markdown("""
<div class="platform-badges">
    <span class="pbadge pb-yt">▶ YouTube</span>
    <span class="pbadge pb-ig">◉ Instagram</span>
    <span class="pbadge pb-tt">◈ TikTok</span>
    <span class="pbadge" style="background:rgba(0,255,157,0.1);color:#00ff9d;border:1px solid rgba(0,255,157,0.3);">+ 1000 Sayt</span>
</div>
""", unsafe_allow_html=True)

# ── CARD: URL + Format ──
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown('<div class="section-label">🔗 Media URL</div>', unsafe_allow_html=True)
url = st.text_input("", placeholder="https://www.youtube.com/watch?v=... və ya Instagram/TikTok linki", label_visibility="collapsed")

st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-label">📦 Format</div>', unsafe_allow_html=True)
    fmt = st.radio("", ["MP4 (Video)", "MP3 (Musiqi)"], horizontal=False, label_visibility="collapsed")
    fmt_clean = "MP4" if "MP4" in fmt else "MP3"

with col2:
    st.markdown('<div class="section-label">🎚️ Keyfiyyət</div>', unsafe_allow_html=True)
    if fmt_clean == "MP4":
        quality = st.selectbox("", ["1080p", "720p", "480p"], label_visibility="collapsed")
    else:
        quality = "best"
        st.markdown('<p style="color:#7ab3cc; font-size:0.9rem; margin-top:0.5rem;">192 kbps · Stereo</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── CARD: Robot Check ──
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">🔐 Təhlükəsizlik Yoxlaması</div>', unsafe_allow_html=True)

human_confirmed = st.checkbox("✅  Mən robot deyiləm — bu yükləməni şüurlu şəkildə həyata keçirirəm")

if human_confirmed:
    st.markdown('<p style="color:#00ff9d; font-size:0.9rem; margin-top:0.3rem;">🟢 Təsdiqləndi — sistem hazırdır.</p>', unsafe_allow_html=True)
else:
    st.markdown('<p style="color:#7ab3cc; font-size:0.85rem; margin-top:0.3rem;">☐ Zəhmət olmasa yuxarıdakı qutuyu işarələyin.</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── DOWNLOAD BUTTON ──
if st.button("⬇  YÜKLƏ  ⬇", disabled=not (url and human_confirmed)):
    if not url.strip():
        st.markdown('<div class="status-error">⚠️ Zəhmət olmasa keçərli bir URL daxil edin.</div>', unsafe_allow_html=True)
    else:
        with st.spinner("🌐 Sistem bağlanır... məlumat çıxarılır..."):
            success, msg, filepath = download_media(url.strip(), fmt_clean, quality)

        if success and filepath and os.path.isfile(filepath):
            st.markdown(f'<div class="status-success">{msg}</div>', unsafe_allow_html=True)
            with open(filepath, "rb") as f:
                file_bytes = f.read()

            fname = os.path.basename(filepath)
            mime = "audio/mpeg" if fmt_clean == "MP3" else "video/mp4"

            st.download_button(
                label=f"💾 {fname} — Kompüterə Yüklə",
                data=file_bytes,
                file_name=fname,
                mime=mime,
            )

            # Auto-delete from server
            try:
                os.remove(filepath)
            except Exception:
                pass

        elif success:
            st.markdown(f'<div class="status-success">{msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-error">{msg}</div>', unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div style="text-align:center; margin-top:3rem; padding: 1rem 0;">
    <p style="font-family:'Orbitron',monospace; font-size:0.6rem; letter-spacing:3px; color:#2a4a5e; text-transform:uppercase;">
        SSSMurad Ultra Downloader · Powered by yt-dlp · Anti-Block Edition
    </p>
    <p style="font-size:0.75rem; color:#2a4a5e; margin-top:0.3rem;">
        Yalnız icazəli məzmun üçün istifadə edin · For authorized content only
    </p>
</div>
""", unsafe_allow_html=True)
