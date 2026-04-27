import streamlit as st
import yt_dlp
import os
from datetime import datetime
import random

# Səhifə Ayarları
st.set_page_config(page_title="Murad AI - Ultra Downloader", page_icon="⚡", layout="wide")

# Müasir Neon Dark CSS
st.markdown("""
    <style>
    .stApp {
        background: #0a0a0a;
        color: #e2e8f0;
    }
    .main-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 40px;
        border: 1px solid #3b82f6;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.2);
    }
    .stButton>button {
        background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        border-radius: 15px;
        padding: 15px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.5);
    }
    .exam-timer {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
        padding: 20px;
        border-radius: 20px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Funksiya: Motivasiya Mesajları
quotes = [
    "Az qaldı Murad, iyunun 7-si sənin günün olacaq! 🎓",
    "Bu gün həll etdiyin bir test, sabahın universitet qapısıdır. 📚",
    "Kod yazmaq hünər istəyir, sən bunu bacarırsan! 💻",
    "Yorulduğunda dincəl, amma imtina etmə. ✨",
    "Mercedes W211-in xəyalı ilə dərslərə davam! 🚗"
]

# Sidebar - İdarə Paneli
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/download.png")
    st.title("🛡️ Murad AI Panel")
    
    # Canlı Geri Sayım
    exam_date = datetime(2026, 6, 7)
    delta = exam_date - datetime.now()
    st.markdown(f"""
    <div class="exam-timer">
        <h3 style='color: #ef4444; margin:0;'>{delta.days} GÜN</h3>
        <p style='margin:0; font-size: 14px;'>Blok İmtahanına Qaldı</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.write(f"📅 Tarix: {datetime.now().strftime('%d.%m.%Y')}")
    st.write(f"⏰ Bakı Vaxtı: {datetime.now().strftime('%H:%M')}")

# Əsas Ekran
st.title("🚀 SSSMurad - Media Downloader")
st.info(random.choice(quotes))

# Yükləmə Bölməsi
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    url = st.text_input("🔗 Instagram / TikTok / YouTube Linki:", placeholder="Link bura yapışdırılır...")
    
    c1, c2 = st.columns(2)
    with c1:
        fmt = st.selectbox("Format:", ["🎬 Video (MP4)", "🎵 Musiqi (MP3)"])
    with c2:
        qual = st.selectbox("Keyfiyyət:", ["Ən Yaxşı", "1080p", "720p", "480p"])

    if st.button("🔥 İNDİ YÜKLƏ"):
        if url:
            try:
                with st.spinner("Murad AI sizin üçün bazadan çəkir... ✨"):
                    # Instagram Fix üçün ən güclü Headers
                    ydl_opts = {
                        'outtmpl': 'downloads/%(title)s.%(ext)s',
                        'http_headers': {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            'Accept': '*/*',
                            'Referer': 'https://www.instagram.com/',
                        },
                        'extractor_args': {'instagram': {'get_video_id': ['web_api']}},
                    }

                    if "Musiqi" in fmt:
                        ydl_opts['format'] = 'bestaudio/best'
                        ydl_opts['postprocessors'] = [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }]
                    else:
                        res = {"1080p": "1080", "720p": "720", "480p": "480"}.get(qual, "best")
                        ydl_opts['format'] = f'bestvideo[height<={res}]+bestaudio/best/best'

                    if not os.path.exists('downloads'): os.makedirs('downloads')

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        f_name = ydl.prepare_filename(info)
                        if "Musiqi" in fmt: f_name = os.path.splitext(f_name)[0] + ".mp3"

                    with open(f_name, "rb") as f:
                        st.download_button("📥 Faylı Cihaza Saxla", f, file_name=os.path.basename(f_name))
                    
                    st.success("Yükləmə uğurla tamamlandı! ✅")
                    os.remove(f_name)

            except Exception as e:
                st.error(f"Xəta: Instagram serverləri hazırda blok tətbiq edir. Bir az sonra yoxlayın və ya başqa link sınayın. \n\nDetallar: {e}")
        else:
            st.warning("Link daxil etmədiniz! ⚠️")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; margin-top: 50px; opacity: 0.5;'>Murad AI Portal v2.0 | Universitet Yolunda Uğurlar!</p>", unsafe_allow_html=True)
