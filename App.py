 import streamlit as st
from gtts import gTTS
import io
import requests

st.set_page_config(page_title="All-in-One AI Studio", page_icon="🎬", layout="centered")

st.title("🎬 All-in-One Free AI Studio")
st.write("यहाँ से आप मुफ़्त में AI Voice और AI Animated Videos/GIFs जनरेट कर सकते हैं!")

# Tabs for features
tab1, tab2 = st.tabs(["🔊 Text to Voice (ऑडियो)", "🎥 Text to Video/Animation (वीडियो)"])

# ----------------- TAB 1: TEXT TO VOICE -----------------
with tab1:
    st.header("Text to Speech")
    text_input = st.text_area("अपना टेक्स्ट यहाँ लिखें:", "नमस्ते, आपकी AI Studio वेबसाइट में आपका स्वागत है!")
    lang = st.selectbox("भाषा चुनें:", ["hi", "en", "es", "fr"], format_func=lambda x: "Hindi" if x=="hi" else ("English" if x=="en" else x))
    
    if st.button("Generate Voice"):
        if text_input.strip() != "":
            with st.spinner("ऑडियो तैयार हो रहा है..."):
                tts = gTTS(text=text_input, lang=lang)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                st.audio(fp, format="audio/mp3")
                st.success("ऑडियो तैयार है! ऊपर 3-dots से डाउनलोड करें।")
        else:
            st.warning("कृपया कुछ टेक्स्ट लिखें।")

# ----------------- TAB 2: TEXT TO VIDEO -----------------
with tab2:
    st.header("Text to AI Video/Animation")
    st.write("अंग्रेज़ी (English) में प्रॉम्ट लिखें ताकि AI बेहतर वीडियो एनिमेशन बना सके।")
    
    video_prompt = st.text_input("Video Prompt:", "A cute robot waving hello, 3d animation style")
    
    if st.button("Generate Video"):
        if video_prompt.strip() != "":
            with st.spinner("AI वीडियो एनिमेशन तैयार कर रहा है (इसमें कुछ सेकंड लग सकते हैं)..."):
                try:
                    # Requesting HuggingFace Animated GIF/Video model
                    API_URL = "https://api-inference.huggingface.co/models/JulienKay/animov-512x512"
                    response = requests.post(API_URL, json={"inputs": video_prompt})
                    
                    if response.status_code == 200:
                        st.image(response.content, caption=f"Prompt: {video_prompt}", use_column_width=True)
                        st.success("वीडियो एनिमेशन तैयार है! इमेज पर लॉन्ग-प्रेस करके सेव/डाउनलोड करें।")
                    else:
                        st.error("सर्वर बिज़ी है या मॉडल लोड हो रहा है, कृपया 10-15 सेकंड बाद फिर कोशिश करें।")
                except Exception as e:
                    st.error("वीडियो जनरेट करने में समस्या आई। कृपया फिर प्रयास करें।")
        else:
            st.warning("कृपया वीडियो का प्रॉम्ट लिखें।")
