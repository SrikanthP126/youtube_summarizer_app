import requests
import streamlit as st
from deep_translator import GoogleTranslator
import pandas as pd

def summarize_text(text, video_title):
    """Summarize Text using Groq API"""
    try:
        if "api_key" not in st.session_state or not st.session_state.api_key:
            return "⚠️ Missing API Key"

        headers = {
            "Authorization": f"Bearer {st.session_state.api_key}",
            "Content-Type": "application/json"
        }

        prompt = f"""
    You are an AI assistant trained to summarize YouTube video transcripts with detailed explanations.
    Your task is to **extract key insights, explain concepts in detail with real time examples to unserstand better than the original content, and provide a concise summary of the video transcript**.
    Summarize the YouTube video: **{video_title}**.
    📌 **Guidelines for Summarization:**
    - Provide an **overview of the video’s core message**.
    - **Break down key concepts** as they were explained in the video, using clear explanations.
    - Use **examples or analogies** from the transcript (if present) to illustrate the ideas.
    - **Maintain timestamps** to show where major points are discussed.
    - If the video includes **step-by-step instructions, frameworks, or key takeaways**, present them clearly.
    - **Avoid generic summaries**—instead, deliver an **educational-style breakdown**.

    📌 **Structured Summary Format:**
    1️⃣ **Introduction & Context:** What is the video about? explain concepts in detail with real time examples to unserstand better than the original content, and provide a concise summary of the video transcript.
    2️⃣ **Key Concepts & Insights:** Summarize major ideas in a way that helps a beginner understand.
    3️⃣ **Step-by-Step Explanations:** If the video teaches something, outline the process or method in a structured way.
    4️⃣ **Important Quotes or Examples:** Capture any relevant analogies, frameworks, or real-world applications.
    5️⃣ **Conclusion & Final Takeaways:** Summarize the main lesson or final message of the video.

    Here is the transcript: {text}
    """
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

        if response.status_code == 429:
            return "❌ Too Many Requests - Rate limit exceeded for Groq API."
        elif response.status_code == 401:
            return "❌ Invalid API Key - Please check your Groq API Key."
        
        response.raise_for_status()

        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "⚠️ Unexpected API Response")
        
    except requests.exceptions.RequestException as e:
        return f"❌ API Request Error: {e}"

    except Exception as e:
        return f"⚠️ General Error: {str(e)}"

        

# def translate_summary(summary_text, target_language):
#     """
#     Translates the given summary text into the target language.
    
#     Parameters:
#         summary_text (str): The text to translate.
#         target_language (str): The target language (e.g., 'fr' for French).
    
#     Returns:
#         str: Translated text.
#     """
#     try:
#         translated_text = GoogleTranslator(source='auto', target=target_language).translate(summary_text)
#         return translated_text
#     except Exception as e:
#         return f"Translation failed: {str(e)}"


#     except requests.exceptions.RequestException as e:
#         return f"❌ API Request Error: {e}"

#     except Exception as e:
#         return f"⚠️ General Error: {str(e)}"
    
def translate_summary(summary_text, target_language):
    """ Translates the given summary text into the target language. """
    try:
        return GoogleTranslator(source='auto', target=target_language).translate(summary_text)
    except Exception as e:
        return f"Translation failed: {str(e)}"

