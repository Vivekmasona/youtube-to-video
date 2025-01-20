import streamlit as st
from yt_dlp import YoutubeDL
import os
import json
import urllib.parse

# Define base URL where the files will be hosted
BASE_URL = "https://vivekfy-api.streamlit.app"  # Replace with your actual hosted URL

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
            download_url = f"{BASE_URL}/downloads/{urllib.parse.quote(file_name)}"

        # Construct JSON response
        response = {
            "success": True,
            "title": video_title,
            "download_url": download_url
        }
        st.json(response)

    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e)
        }
        st.json(error_response)
else:
    st.json({
        "success": False,
        "error": "Please provide a valid YouTube URL using '?url=YOUR_YOUTUBE_URL'"
    })
