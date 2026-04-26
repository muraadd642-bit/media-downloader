import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Murad AI Downloader", page_icon="🚀")

# Dizayn (CSS) - Hooligan/Dark Style
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 10px; height: 3em; font-weight: bold; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border: 1px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Murad AI Media Downloader")
st.write("Sistem aktivdir. Linki yapışdır və yüklə!")

url = st.text_input("Linki bura daxil et:", placeholder="Instagram, TikTok və ya YouTube...")
format_type = st.radio("Format seç:", ["🎬 Video (MP4)", "🎵 Musiqi (MP3)"])

if st.button("Yükləməyə Başla"):
    if url:
        try:
            with st.spinner("Bazadan çəkilir... Gözləyin. 🛠️"):
                ydl_opts = {
                    'format': 'best' if "Video" in format_type else 'bestaudio/best',
                    'outtmpl': 'downloads/%(title)s.%(ext)s',
                }
                if "Musiqi" in format_type:
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]

                if not os.path.exists('downloads'): os.makedirs('downloads')

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    if "Musiqi" in format_type:
                        filename = os.path.splitext(filename)[0] + ".mp3"

                with open(filename, "rb") as f:
                    st.download_button(label="📥 Faylı Telefona/PC-yə Köçür", data=f, file_name=os.path.basename(filename))
                
                st.success("Hazırdır! ✅")
                os.remove(filename)
        except Exception as e:
            st.error(f"Xəta: {e}")
    else:
        st.warning("Link daxil etmədin! ⚠️")
