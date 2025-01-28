import streamlit as st
from yt_dlp import YoutubeDL

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
            # Construct the API URL
            api_url = f"https://vivekfy.vercel.app/received?url={playback_url}"

            # Redirect user to the constructed URL
            st.write("Redirecting...")
            st.experimental_set_query_params(url=playback_url)  # Update query params
            st.markdown(f"[Click here if not redirected automatically]({api_url})")  # Fallback link
            st.stop()  # Stop further execution after redirecting

        else:
            st.error("Could not retrieve playback URL")

    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.warning("No URL provided. Use '?url=YOUTUBE_URL' in the query.")
