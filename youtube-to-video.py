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
            # Redirect to playback URL
            redirect_html = f"""
            <meta http-equiv="refresh" content="0; url={playback_url}" />
            <p>Redirecting to playback URL: <a href="{playback_url}">{playback_url}</a></p>
            """
            st.markdown(redirect_html, unsafe_allow_html=True)

        else:
            st.error("Could not retrieve playback URL")

    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.warning("No URL provided. Use '?url=YOUTUBE_URL' in the query.")
