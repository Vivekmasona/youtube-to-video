import streamlit as st
from yt_dlp import YoutubeDL
import subprocess
import os

# Parse query parameters
query_params = st.experimental_get_query_params()
youtube_url = query_params.get("url", [None])[0]

if youtube_url:
    try:
        # yt-dlp options for extracting playback URL and metadata
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': 'downloaded_audio.%(ext)s',  # Save file locally
            'postprocessors': [{
                'key': 'FFmpegMetadata'
            }]
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            audio_filename = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            title = info_dict.get('title', 'Unknown Title')
            thumbnail_url = info_dict.get('thumbnail', '')

        # Download thumbnail
        thumbnail_filename = "thumbnail.jpg"
        os.system(f"wget -O {thumbnail_filename} {thumbnail_url}")

        # Add text overlay to thumbnail using ffmpeg
        edited_thumbnail = "edited_thumbnail.jpg"
        overlay_text = "Vivek Masona"
        ffmpeg_text_cmd = f"""
        ffmpeg -i {thumbnail_filename} -vf "drawtext=text='{overlay_text}':fontcolor=white:fontsize=24:x=10:y=10" {edited_thumbnail} -y
        """
        os.system(ffmpeg_text_cmd)

        # Embed edited thumbnail & update metadata
        final_audio = "final_audio.mp3"
        ffmpeg_metadata_cmd = f"""
        ffmpeg -i {audio_filename} -i {edited_thumbnail} -map 0:a -map 1 -metadata title="{title}" -metadata artist="Vivek Masona" -id3v2_version 3 {final_audio} -y
        """
        os.system(ffmpeg_metadata_cmd)

        # Provide Download Link
        with open(final_audio, "rb") as f:
            st.download_button(label="Download Audio", data=f, file_name=f"{title}.mp3", mime="audio/mpeg")

        st.success("Audio processed and ready for download!")

    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.warning("No URL provided. Use '?url=YOUTUBE_URL' in the query.")
