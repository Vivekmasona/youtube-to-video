import streamlit as st
from yt_dlp import YoutubeDL
import json

# Parse query parameters
query_params = st.experimental_get_query_params()
youtube_url = query_params.get("url", [None])[0]

if youtube_url:
    try:
        # yt-dlp options for extracting URL without downloading
        ydl_opts = {
            'format': 'bestaudio/best',  # Get best audio or single file
            'quiet': True,  # Suppress verbose output
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)  # No download
            playback_url = info_dict.get('url', None)  # Direct playback URL
            title = info_dict.get('title', 'Unknown Title')

        if playback_url:
            response = {
                "status": "success",
                "title": title,
                "playback_url": playback_url
            }
        else:
            response = {
                "status": "error",
                "message": "Could not retrieve playback URL"
            }

    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }

else:
    response = {
        "status": "error",
        "message": "No URL provided. Use '?url=YOUTUBE_URL' in the query."
    }

# Display response as JSON
st.json(response)
