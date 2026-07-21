import streamlit as st
from gtts import gTTS
import io
import urllib.parse
import requests

# Page Configuration
st.set_page_config(page_title="All-in-One AI Studio", page_icon="⚡", layout="wide")

st.title("⚡ Ultimate Free AI Studio")
st.write("एक ही जगह पर AI Voice, YouTube/Instagram Thumbnails और AI Video/Animation बनाएँ!")

# Tabs Hierarchy
tab1, tab2, tab3 = st.tabs([
    "🔊 Multi-Lang Text to Voice", 
    "🖼️ Thumbnail & Image AI Generator", 
    "🎥 AI Video / Animation"
])

# ----------------- TAB 1: TEXT TO VOICE (MULTI-LANGUAGE) -----------------
with tab1:
    st.header("🔊 Voice Generator (Text to Speech)")
    st.write("अपनी पसंद की भाषा में टेक्स्ट से आवाज़ (Audio) बनाएँ:")
    
    text_input = st.text_area("अपना टेक्स्ट लिखें:", "नमस्ते! आपकी AI Studio में आपका स्वागत है।", height=100)
    
    # Language Selection
    languages = {
        "Hindi (हिंदी)": "hi",
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Tamil (தமிழ்)": "ta",
        "Bengali (বাংলা)": "bn"
    }
    
    selected_lang = st.selectbox("भाषा (Language) चुनें:", list(languages.keys()))
    lang_code = languages[selected_lang]
    
    if st.button("🎙️ Generate Voice"):
        if text_input.strip() != "":
            with st.spinner("ऑडियो तैयार हो रहा है..."):
                try:
                    tts = gTTS(text=text_input, lang=lang_code)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    st.audio(fp, format="audio/mp3")
                    st.success("✅ ऑडियो तैयार है! ऊपर 3-dots पर क्लिक करके डाउनलोड करें।")
                except Exception as e:
                    st.error("ऑडियो जनरेट करने में समस्या आई।")
        else:
            st.warning("कृपया कुछ टेक्स्ट लिखें।")

# ----------------- TAB 2: THUMBNAIL & IMAGE GENERATOR -----------------
with tab2:
    st.header("🖼️ AI Thumbnail & Image Generator")
    st.write("YouTube, Instagram या सोशल मीडिया के लिए HD Thumbnails और Images बनाएँ।")
    
    img_prompt = st.text_input("Prompt लिखें (English में):", "A glowing futuristic cyber robot, high details, 4k thumbnail")
    
    # Aspect Ratio for YouTube / Instagram
    platform = st.selectbox("किस प्लेटफ़ॉर्म के लिए बनाना है?", [
        "YouTube Thumbnail (16:9)", 
        "Instagram Post / Square (1:1)", 
        "Instagram Reel / Story (9:16)"
    ])
    
    # Dimension calculation
    if platform == "YouTube Thumbnail (16:9)":
        width, height = 1280, 720
    elif platform == "Instagram Reel / Story (9:16)":
        width, height = 720, 1280
    else:
        width, height = 1024, 1024

    if st.button("✨ Generate Image / Thumbnail"):
        if img_prompt.strip() != "":
            with st.spinner("AI इमेज तैयार कर रहा है (3-5 सेकंड)..."):
                try:
                    encoded_prompt = urllib.parse.quote(img_prompt)
                    media_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
                    
                    st.image(media_url, caption=f"Platform: {platform} | Prompt: {img_prompt}", use_column_width=True)
                    st.success("✅ इमेज तैयार है! इमेज पर लॉन्ग-प्रेस या राइट-क्लिक करके सेव कर लें।")
                except Exception as e:
                    st.error("इमेज जनरेट करने में समस्या आई।")
        else:
            st.warning("कृपया प्रॉम्ट लिखें।")

# ----------------- TAB 3: AI VIDEO GENERATOR -----------------
with tab3:
    st.header("🎥 AI Video / Animation Generator")
    st.write("अंग्रेज़ी (English) में प्रॉम्ट लिखकर एनिमेटेड AI Visuals जनरेट करें।")
    
    video_prompt = st.text_input("Video Prompt:", "A cute panda dancing in the forest, 3d animation")
    
    if st.button("🎬 Generate Video"):
        if video_prompt.strip() != "":
            with st.spinner("AI वीडियो तैयार कर रहा है..."):
                try:
                    API_URL = "https://api-inference.huggingface.co/models/cerspense/zeroscope_v2_576w"
                    response = requests.post(API_URL, json={"inputs": video_prompt}, timeout=35)
                    
                    if response.status_code == 200:
                        st.image(response.content, caption=f"Prompt: {video_prompt}", use_column_width=True)
                        st.success("✅ एनिमेशन तैयार है! डाउनलोड करने के लिए इमेज को सेव करें।")
                    else:
                        st.warning("वीडियो सर्वर अभी बिज़ी है। आप 'Thumbnail/Image Generator' टैब से भी बेहतरीन विजुअल्स तुरंत बना सकते हैं!")
                except Exception as e:
                    st.error("वीडियो सर्वर टाइम-आउट हो गया। कृपया दोबारा कोशिश करें।")
        else:
            st.warning("कृपया प्रॉम्ट लिखें।")
