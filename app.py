import os
import requests
import streamlit as st
from dotenv import load_dotenv
from utils.youtube_utils import extract_video_id, get_video_title, fetch_youtube_transcript
from utils.groq_utils import summarize_text, translate_summary

# Load environment variables
load_dotenv()
YOUR_YOUTUBE_API_KEY = os.getenv("YOUR_YOUTUBE_API_KEY")
# 🔹 Set YouTube Favicon
st.set_page_config(page_title="YouTube Summarizer", page_icon="🎥", layout="wide")

# 🔹 Page Header
st.title("▶️ YouTube Video Summarizer with Groq AI")

# 🔹 Sidebar: API Key Entry
st.sidebar.subheader("📂 Chat History")

# ✅ Store Chat History in Session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

# ✅ Handle API Key (One-time entry)
if "api_key" not in st.session_state:
    groq_api_key = st.sidebar.text_input("🔑 Enter Groq API Key:", type="password")
    if groq_api_key:
        st.session_state.api_key = groq_api_key
        st.rerun()
else:
    st.sidebar.success("✅ API Key Set")

# ✅ Language Selection for Summary
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "Hindi": "hi",
    "Telugu": "te",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Japanese": "ja",
    "Korean": "ko",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Arabic": "ar",
    "Bengali": "bn",
    "Tamil": "ta",
    "Turkish": "tr",
    "Urdu": "ur",
    "Malay": "ms",
    "Dutch": "nl",
    "Greek": "el",
    "Polish": "pl",
    "Hebrew": "he",
    "Swedish": "sv",
    "Thai": "th",
    "Vietnamese": "vi",
    "Filipino": "tl"
}
selected_language = st.sidebar.selectbox("🌍 Choose Summary Language:", list(languages.keys()))

# ✅ Sidebar: Load Chat History with Correct Titles
for video_title, summary in st.session_state.chat_history.items():
    if st.sidebar.button(video_title, key=video_title):
        st.session_state["last_summary"] = summary
        st.session_state["last_video_title"] = video_title

# ✅ New Chat Button
if st.sidebar.button("🆕 New Chat"):
    st.session_state["last_summary"] = ""
    st.session_state["last_video_title"] = ""
    st.rerun()

# ✅ Main Section: YouTube Video Input
video_url = st.text_input("📌 Enter YouTube Video URL to Summarize:", key="video_url")

if video_url:
    video_id = extract_video_id(video_url)

    if video_id:
        with st.spinner("🔍 Fetching video title..."):
            video_title = get_video_title(video_id) #YOUR_YOUTUBE_API_KEY)

        with st.spinner("🎙️ Fetching transcript..."):
            transcript_text = fetch_youtube_transcript(video_id)

        if "Error" in transcript_text:
            st.error(transcript_text)
        else:
            # Summarize Video
            with st.spinner("📝 Generating Summary..."):
                summary = summarize_text(transcript_text, video_title)

            # Translate Summary if Needed
            if selected_language != "English":
                with st.spinner(f"🌎 Translating Summary to {selected_language}..."):
                    summary = translate_summary(summary, languages[selected_language])

            # ✅ Store Chat History
            st.session_state.chat_history[video_title] = summary
            st.session_state["last_summary"] = summary
            st.session_state["last_video_title"] = video_title

            # st.subheader(f"📜 Video Summary")
            st.subheader(f"📜 {video_title} - Summary")
            st.write(summary)

# ✅ Follow-up Question Section
if "last_summary" in st.session_state and st.session_state["last_summary"]:
    st.subheader("💬 Need Further Explanation?")
    user_question = st.text_input("Ask any follow-up questions:", key="followup_question")

    if user_question:
        with st.spinner("🤔 Thinking..."):
            followup_response = summarize_text(user_question, st.session_state["last_video_title"])
            st.subheader("🔍 Clarification Response")
            st.write(followup_response)
