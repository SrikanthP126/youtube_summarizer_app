import os
from dotenv import load_dotenv
import requests
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()
YOUR_YOUTUBE_API_KEY = os.getenv("YOUR_YOUTUBE_API_KEY")
def extract_video_id(url):
    """Extract YouTube Video ID from URL"""
    try:
        if "youtube.com/watch?v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        else:
            return None
    except:
        return None

def get_video_title(video_id):
    """Fetch Video Title using YouTube API"""
    try:
        api_key = os.getenv("YOUR_YOUTUBE_API_KEY")  
        if not api_key:
            return "⚠️ YouTube API Key Missing"

        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
        response = requests.get(url)
        
        if response.status_code == 403:
            return "❌ API Key Quota Exceeded - Try another key."
        elif response.status_code == 401:
            return "❌ Invalid YouTube API Key."
        
        response.raise_for_status()

        data = response.json()
        return data.get("items", [{}])[0].get("snippet", {}).get("title", "⚠️ Title Not Found")

    except requests.exceptions.RequestException as e:
        return f"⚠️ YouTube API Error: {e}"


# def get_video_title(video_id, api_key):
#     """Fetch Video Title using YouTube API"""
#     try:
#         api_key = "YOUR_YOUTUBE_API_KEY"  
#         url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()

#         if "items" in data and len(data["items"]) > 0:
#             return data["items"][0]["snippet"]["title"]
#         else:
#             return "⚠️ Title Not Found"

    except requests.exceptions.RequestException as e:
        return f"⚠️ YouTube API Error: {e}"

def fetch_youtube_transcript(video_id):
    """Fetch YouTube Video Transcript"""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return "\n".join([f"[{item['start']:.2f}s] {item['text']}" for item in transcript])
    except:
        return "⚠️ Error fetching transcript"
