import streamlit as st
from yt_dlp import YoutubeDL
import requests

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
            info_dict = ydl.extract_info(youtube_url, download=False)  # Extract info
            playback_url = info_dict.get('url', None)

        if playback_url:
            # Automatically send playback_url to your API
            api_url = f"https://vivekfy.vercel.app/received?url={playback_url}"
            try:
                response = requests.get(api_url)  # Send request to your API
                if response.status_code == 200:
                    st.success(f"Playback URL sent to API: {playback_url}")
                else:
                    st.error(f"Failed to send playback URL to API: {response.status_code}")
            except Exception as api_error:
                st.error(f"Error calling API: {api_error}")

            # Stream the audio directly in Streamlit
            st.audio(playback_url)

        else:
            st.error("Could not retrieve playback URL")

    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.warning("No URL provided. Use '?url=YOUTUBE_URL' in the query.")
