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
            title = info_dict.get('title', 'Unknown Title')
            thumbnail = info_dict.get('thumbnail', '')

        if playback_url:
            # Prepare JSON payload
            payload = {
                "url": playback_url,
                "title": title,
                "thumbnail": thumbnail
            }

            # Vercel API URL
            api_url = "https://your-vercel-api.vercel.app/receive"

            # Send JSON data to the backend
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                st.success("Playback data sent successfully!")
            else:
                st.error(f"Failed to send data: {response.status_code} - {response.text}")

            # Optionally stream the audio
            st.audio(playback_url)

        else:
            st.error("Could not retrieve playback URL")

    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.warning("No URL provided. Use '?url=YOUTUBE_URL' in the query.")
