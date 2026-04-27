import streamlit as st
import yt_dlp
import os
from datetime import datetime
import random

# Səhifənin Əsas Ayarları
st.set_page_config(page_title="SSSMurad - Media Downloader", page_icon="⚡", layout="wide")

# Müasir Neon və Şüşə (Glassmorphism) Dizaynı
st.markdown("""
    <style>
    .stApp {
        background: #0f172a;
        color: #f8fafc;
    }
    .main-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 35px;
        border: 1px solid rgba(59, 130, 246, 0.3);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
        color: white;
        border-radius: 12px;
        padding: 12px;
        font-size: 16px;
        font-weight: 800;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
    }
    .countdown-box {
        background: rgba(239, 68, 68, 0.15);
        border-left: 4px solid #ef4444;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Motivasiya Cümlələri
quotes = [
    "Uğur zəhmət tələb edir. Davam et! 🚀",
    "Kod yazmaq və məqsədə çatmaq eyni fəlsəfədir: Xətaları tap və düzəlt. 💻",
    "Hədəfə gedən yolda kiçik fasilələr ancaq sürət yığmaq üçündür. 🏎️",
    "Bu günün zəhməti, sabahın tələbə biletidir. 🎓"
]

# Yan Panel (Sidebar) - Portal İdarəetməsi
with st.sidebar:
    st.title("🛡️ Murad AI Portal")
    st.markdown("---")
    
    # 7 İyun Hədəfi üçün Canlı Taymer
    exam_date = datetime(2026, 6, 7)
    delta = exam_date - datetime.now()
    
    st.markdown(f"""
    <div class="countdown-box">
        <h2 style='color: #ef4444; margin:0;'>{delta.days} GÜN</h2>
        <p style='margin:0; font-size: 13px; color: #cbd5e1;'>Blok İmtahanına Qaldı</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.write(f"📅 Tarix: {datetime.now().strftime('%d.%m.%Y')}")
    st.write(f"⏰ Bakı Vaxtı: {datetime.now().strftime('%H:%M')}")

# Əsas Səhifə Başlığı
st.title("⚡ SSSMurad - Media Downloader")
st.info(random.choice(quotes))

# Yükləmə Paneli
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    url = st.text_input("🔗 Media Linki (Instagram, TikTok, YouTube):", placeholder="https://...")
    
    col1, col2 = st.columns(2)
    with col1:
        fmt_choice = st.selectbox("Format:", ["🎬 Video (MP4)", "🎵 Musiqi (MP3)"])
    with col2:
        qual_choice = st.selectbox("Keyfiyyət (Video üçün):", ["Ən Yaxşı", "1080p", "720p", "480p"])

    if st.button("🔥 HAZIRLA VƏ YÜKLƏ"):
        if url:
            try:
                with st.spinner("Sistem faylı çəkir, zəhmət olmasa gözləyin... ⏳"):
                    
                    # Keyfiyyət məntiqinin xətasız qurulması
                    if qual_choice == "Ən Yaxşı":
                        video_format = "bestvideo+bestaudio/best"
                    else:
                        res = qual_choice.replace("p", "")
                        video_format = f"bestvideo[height<={res}]+bestaudio/best"

                    # Sistem Ayarları və Anti-Blok mexanizmi
                    ydl_opts = {
                        'outtmpl': 'downloads/%(title)s.%(ext)s',
                        'quiet': True,
                        'no_warnings': True,
                        'http_headers': {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                        },
                        'extractor_args': {
                            'instagram': {'get_video_id': ['web_api']}
                        }
                    }

                    # Əgər musiqi seçilibsə
                    if "Musiqi" in fmt_choice:
                        ydl_opts['format'] = 'bestaudio/best'
                        ydl_opts['postprocessors'] = [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }]
                    else:
                        ydl_opts['format'] = video_format

                    # Yükləmə qovluğunu yoxla və yarat
                    if not os.path.exists('downloads'):
                        os.makedirs('downloads')

                    # Faylı yüklə
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        file_path = ydl.prepare_filename(info)
                        if "Musiqi" in fmt_choice:
                            file_path = os.path.splitext(file_path)[0] + ".mp3"

                    # İstifadəçiyə təqdim et
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="📥 CİHAZA YÜKLƏ",
                            data=f,
                            file_name=os.path.basename(file_path),
                            mime="video/mp4" if "Video" in fmt_choice else "audio/mpeg"
                        )
                    
                    st.success("✅ Proses uğurla bitdi! Faylı yuxarıdakı düymədən cihazınıza saxlaya bilərsiniz.")
                    
                    # Server yaddaşını təmizlə
                    os.remove(file_path)

            except Exception as e:
                st.error("⚠️ Instagram və ya digər platforma serveri bloka saldı. Başqa bir link yoxlayın və ya bir neçə dəqiqə gözləyin.")
                with st.expander("Texniki Detallar (Ancaq Admin Üçün)"):
                    st.code(e)
        else:
            st.warning("⚠️ Zəhmət olmasa bir link daxil edin!")
            
    st.markdown('</div>', unsafe_allow_html=True)
