import streamlit as st
from yt_dlp import YoutubeDL
import requests

# Parse query parameters
query_params = st.experimental_get_query_params()
youtube_url = query_params.get("url", [None])[0]

if youtube_url:
    try:
        # yt-dlp options for extracting playback URL
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            playback_url = info_dict.get('url', None)

        if playback_url:
            # Encode playback URL for safe transmission
            encoded_url = requests.utils.quote(playback_url, safe='')

            # Construct the API URL
            api_url = f"https://vivekfy.vercel.app/received?url={encoded_url}"

            # Send the playback URL to the backend
            response = requests.get(api_url)

            if response.status_code == 200:
                st.success(f"Playback URL sent successfully: {playback_url}")
            else:
                st.error(f"Failed to send playback URL: {response.status_code}")

            # Optionally stream the audio
            st.audio(playback_url)

        else:
            st.error("Could not retrieve playback URL")

    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.warning("No URL provided. Use '?url=YOUTUBE_URL' in the query.")
