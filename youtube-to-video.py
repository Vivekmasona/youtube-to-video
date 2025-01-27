import streamlit as st
from yt_dlp import YoutubeDL
import requests
import json

# Parse query parameters
query_params = st.experimental_get_query_params()
youtube_url = query_params.get("url", [None])[0]

def send_to_api(playback_url):
    """Function to send the playback URL to your API."""
    try:
        api_url = f"https://vivekfy.vercel.app/recive?url={playback_url}"
        response = requests.get(api_url)
        return {
            "status_code": response.status_code,
            "response_data": response.json() if response.status_code == 200 else "Failed to get valid response"
        }
    except Exception as e:
        return {"error": str(e)}

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
            title = info_dict.get('title', 'Unknown Title')

        if playback_url:
            api_result = send_to_api(playback_url)  # Automatically trigger API call
            response = {
                "status": "success",
                "title": title,
                "playback_url": playback_url,
                "api_status": api_result.get("status_code"),
                "api_response": api_result.get("response_data")
            }

            # Save the response as url.json
            with open("url.json", "w") as f:
                json.dump(response, f)
            st.success("Playback URL saved as url.json")

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
