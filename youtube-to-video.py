import streamlit as st
from yt_dlp import YoutubeDL
import os
import urllib.parse

# Define base URL of your hosted Streamlit app
BASE_URL = "https://vivekfy-api.streamlit.app"

# Streamlit configuration
st.set_page_config(page_title="YouTube Downloader API", layout="centered")

# Parse URL query parameter
query_params = st.experimental_get_query_params()
youtube_url = query_params.get("url", [None])[0]

if youtube_url:
    try:
        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',  # Best audio or single file
            'outtmpl': './downloads/%(title)s.%(ext)s',  # Save path and file name
            'noplaylist': True,  # Download a single video
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            video_title = info_dict.get('title', 'Unknown Title')
            file_name = os.path.basename(ydl.prepare_filename(info_dict))
            full_url = f"{BASE_URL}/downloads/{urllib.parse.quote(file_name)}"

        # Success message with direct URL
        st.success("Download successful!")
        st.write(f"**Title:** {video_title}")
        st.write(f"**Access your file here:** [Download or Play]({full_url})")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please add '?url=YOUR_YOUTUBE_URL' to use the API.")
