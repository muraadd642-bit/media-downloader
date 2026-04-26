import streamlit as st
import yt_dlp
import os
from datetime import datetime

# Səhifə Ayarları
st.set_page_config(page_title="Murad 642 - Ultra Downloader", page_icon="⚡", layout="wide")

# Müasir CSS Dizaynı
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.3);
    }
    .countdown-box {
        text-align: center;
        padding: 15px;
        background: rgba(59, 130, 246, 0.1);
        border-radius: 15px;
        border: 1px solid #3b82f6;
    }
    </style>
    """, unsafe_allow_html=True)

# Yan Panel (Sidebar) - İmtahan Geri Sayımı
with st.sidebar:
    st.title("🎯 Hədəf 7 İyun")
    exam_date = datetime(2026, 6, 7)
    now = datetime.now()
    delta = exam_date - now
    
    st.markdown(f"""
    <div class="countdown-box">
        <h2 style='color: #3b82f6; margin:0;'>{delta.days} GÜN</h2>
        <p style='margin:0;'>Blok İmtahanına Qaldı</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Unutma: Bu günün zəhməti, sabahın uğurudur! 📚")

# Əsas Hissə
st.title("⚡ Murad AI Ultra Downloader")
st.write("Instagram, TikTok, YouTube və s. — Ən yüksək keyfiyyətdə yüklə.")

with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    url = st.text_input("🔗 Media Linkini Daxil Edin:", placeholder="https://...")
    
    col1, col2 = st.columns(2)
    with col1:
        format_choice = st.selectbox("Format Seçin:", ["Video (MP4)", "Musiqi (MP3)"])
    with col2:
        quality_choice = st.selectbox("Keyfiyyət (Video üçün):", ["Ən Yaxşı", "1080p", "720p", "480p"])

    if st.button("🚀 Hazırla və Yüklə"):
        if url:
            try:
                # Yükləmə tənzimləmələri
                ydl_opts = {
                    'outtmpl': 'downloads/%(title)s.%(ext)s',
                    'quiet': True,
                    'no_warnings': True,
                }

                if format_choice == "Musiqi (MP3)":
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                else:
                    # Keyfiyyətə görə format seçimi
                    q_map = {"1080p": "1080", "720p": "720", "480p": "480"}
                    res = q_map.get(quality_choice, "best")
                    if res == "best":
                        ydl_opts['format'] = 'bestvideo+bestaudio/best'
                    else:
                        ydl_opts['format'] = f'bestvideo[height<={res}]+bestaudio/best'

                with st.spinner("Server emal edir... 🌪️"):
                    if not os.path.exists('downloads'): os.makedirs('downloads')
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        file_path = ydl.prepare_filename(info)
                        if format_choice == "Musiqi (MP3)":
                            file_path = os.path.splitext(file_path)[0] + ".mp3"

                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Faylı Cihaza Köçür",
                            data=f,
                            file_name=os.path.basename(file_path),
                            mime="video/mp4" if "Video" in format_choice else "audio/mpeg"
                        )
                    st.success("Fayl hazırdır!")
                    os.remove(file_path)

            except Exception as e:
                st.error(f"Xəta baş verdi: {e}")
        else:
            st.warning("Zəhmət olmasa link daxil edin!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<p style='text-align: center; color: #64748b;'>Made with ❤️ by Murad AI | 2026</p>", unsafe_allow_html=True)
