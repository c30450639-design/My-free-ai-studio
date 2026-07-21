import streamlit as st
from gtts import gTTS
import io
import urllib.parse

st.set_page_config(page_title="All-in-One AI Studio", page_icon="🎬", layout="centered")

st.title("🎬 All-in-One Free AI Studio")
st.write("यहाँ से आप मुफ़्त में AI Voice और AI Visuals/Videos जनरेट कर सकते हैं!")

# Tabs for features
tab1, tab2 = st.tabs(["🔊 Text to Voice (ऑडियो)", "🎥 Text to Video/Visuals (वीडियो)"])

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
    st.header("Text to AI Video/Visuals")
    st.write("अंग्रेज़ी (English) में प्रॉम्ट लिखें ताकि AI बेहतर रिज़ल्ट बना सके।")
    
    video_prompt = st.text_input("Video Prompt:", "A futuristic robot walking in a cyberpunk city, 3d render")
    
    if st.button("Generate Video"):
        if video_prompt.strip() != "":
            with st.spinner("AI वीडियो एनिमेशन तैयार कर रहा है..."):
                try:
                    # Using Pollinations AI for fast & unlimited generation
                    encoded_prompt = urllib.parse.quote(video_prompt)
                    media_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"
                    
                    st.image(media_url, caption=f"Prompt: {video_prompt}", use_column_width=True)
                    st.success("एनिमेशन/विजुअल तैयार है! इस पर लॉन्ग-प्रेस (या राइट क्लिक) करके डाउनलोड करें।")
                except Exception as e:
                    st.error("जनरेट करने में समस्या आई। कृपया दोबारा कोशिश करें।")
        else:
            st.warning("कृपया प्रॉम्ट लिखें।")
