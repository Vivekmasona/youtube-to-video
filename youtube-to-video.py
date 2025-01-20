import streamlit as st
from yt_dlp import YoutubeDL
import os
import urllib.parse

# Streamlit configuration for API-like usage
st.set_page_config(page_title="YouTube Downloader API", layout="centered")

# Parse URL query parameter
query_params = st.experimental_get_query_params()
youtube_url = query_params.get("url", [None])[0]

# If 'url' is provided in the query, attempt to download and serve the video/audio
if youtube_url:
    try:
        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',  # Best audio or single file
            'outtmpl': './downloads/%(title)s.%(ext)s',  # File path and name format
            'noplaylist': True,  # Download single video
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            video_title = info_dict.get('title', 'Unknown Title')
            file_path = ydl.prepare_filename(info_dict)

        st.success("Download successful!")
        st.write(f"**Title:** {video_title}")
        st.write(f"**Saved to:** {file_path}")

        # Simulate redirect to playback URL (file server alternative)
        file_url = f"/downloads/{urllib.parse.quote(os.path.basename(file_path))}"
        st.write(f"Access your file here: {file_url}")

        # Provide download button as alternative
        with open(file_path, "rb") as f:
            st.download_button(
                label="Download File",
                data=f,
                file_name=os.path.basename(file_path),
                mime="audio/mpeg"  # Adjust mime type if needed
            )

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please add '?url=YOUR_YOUTUBE_URL' to use the API.")
