import streamlit as st
import yt_dlp
import os
from datetime import datetime
import time

# Səhifə Ayarları
st.set_page_config(page_title="SSSMurad AI", page_icon="🤖", layout="wide")

# Müasir CSS
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #ffffff; }
    .main-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid #3b82f6;
    }
    /* Robot deyiləm qutusu üçün stil */
    .captcha-box {
        background: #1a1c23;
        border: 1px solid #444;
        padding: 15px;
        border-radius: 5px;
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🛡️ Murad AI Portal")
    exam_date = datetime(2026, 6, 7)
    days_left = (exam_date - datetime.now()).days
    st.error(f"🚀 Blok İmtahanına: {days_left} GÜN")
    st.markdown("---")
    st.info("Instagram xətası alırsınızsa, cookies.txt faylını yeniləyin.")

st.title("⚡ SSSMurad - Ultra Downloader")

# State (Yaddaş) yaratmaq
if 'is_human' not in st.session_state:
    st.session_state.is_human = False

with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    if not st.session_state.is_human:
        st.subheader("Giriş Təsdiqi")
        # "Mən robot deyiləm" simulyasiyası
        col_c1, col_c2 = st.columns([0.1, 0.9])
        with col_c1:
            check = st.checkbox("", key="robot_check")
        with col_c2:
            st.markdown("🔒 **Mən robot deyiləm**")
        
        if check:
            with st.spinner("Təsdiqlənir..."):
                time.sleep(1)
                st.session_state.is_human = True
                st.rerun()
    else:
        # Əsas Yükləmə Bölməsi
        url = st.text_input("🔗 Media Linkini Daxil Edin:", placeholder="https://...")
        
        col1, col2 = st.columns(2)
        with col1:
            fmt = st.selectbox("Format:", ["Video (MP4)", "Musiqi (MP3)"])
        with col2:
            qual = st.selectbox("Keyfiyyət:", ["1080p", "720p", "480p", "360p"])

        if st.button("🚀 YÜKLƏMƏYƏ BAŞLA"):
            if url:
                try:
                    with st.spinner("Murad AI emal edir... ✨"):
                        ydl_opts = {
                            'outtmpl': 'downloads/%(title)s.%(ext)s',
                            'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
                            'format': f'bestvideo[height<={qual.replace("p","")}]+bestaudio/best' if "Video" in fmt else 'bestaudio/best',
                            'http_headers': {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                            }
                        }
                        
                        if "Musiqi" in fmt:
                            ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]

                        if not os.path.exists('downloads'): os.makedirs('downloads')

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(url, download=True)
                            f_name = ydl.prepare_filename(info)
                            if "Musiqi" in fmt: f_name = os.path.splitext(f_name)[0] + ".mp3"

                        with open(f_name, "rb") as f:
                            st.download_button("📥 Cihaza Saxla", f, file_name=os.path.basename(f_name))
                        
                        st.success("Hazırdır! ✅")
                        os.remove(f_name)
                except Exception as e:
                    st.error(f"Xəta: Instagram bloku hələ də aktivdir. Cookies.txt mütləqdir.")
            else:
                st.warning("Link daxil edin!")
    
    st.markdown('</div>', unsafe_allow_html=True)
