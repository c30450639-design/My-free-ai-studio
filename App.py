import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import io

# Page Config
st.set_page_config(page_title="AI Creator Toolkit 2026", page_icon="🚀", layout="wide")

# Header
st.title("🚀 All-in-One AI Creator Toolkit")
st.write("2026 के सभी ज़रूरतमंद AI टूल्स एक ही जगह पर—बिलकुल मुफ़्त!")

# ----------------- ADSTERRA AD SLOT -----------------
# अपनी Adsterra का 300x250 या Native Banner कोड नीचे पेस्ट करें
adsterra_code = """
<div style="text-align:center;">
    <p style="color:gray; font-size:12px;">Advertisement</p>
    <!-- Paste your Adsterra Code Here -->
</div>
"""
components.html(adsterra_code, height=150)
# ----------------------------------------------------

# Tabs
tab1, tab2, tab3 = st.tabs([
    "🔥 Viral Script & Hook", 
    "🖼️ Image Converter & Resizer", 
    "🎨 Pro Prompt Enhancer"
])

# ----------------- TAB 1: VIRAL SCRIPT GENERATOR -----------------
with tab1:
    st.header("🔥 Viral Script & Hook Generator")
    st.write("YouTube Shorts / Reels के लिए 3 सेकंड में वायरल स्क्रिप्ट्स बनाएं!")
    
    topic = st.text_input("अपने वीडियो का Topic लिखें (e.g., How to earn money online):")
    platform = st.selectbox("प्लैटफॉर्म चुनें:", ["YouTube Shorts", "Instagram Reel", "TikTok"])
    
    if st.button("✨ Generate Script"):
        if topic.strip() != "":
            st.subheader("📌 Catchy Hook (शुरुआत में बोलने के लिए):")
            st.info(f"👉 'क्या आप भी {topic} की यह सीक्रेट ट्रिक नहीं जानते? रुकिए और पूरा वीडियो देखिए!'")
            
            st.subheader("📜 Main Video Script:")
            st.write(f"1. **0-3 sec:** तुरंत ध्यान खींचने वाली लाइन (Hook) बोलें।\n2. **3-15 sec:** {topic} के बारे में मुख्य 2-3 पॉइंट्स बताएं।\n3. **15-30 sec:** कॉल-टू-एक्शन (उदा: 'ऐसे और ट्रिक्स के लिए अभी फॉलो करें!')।")
            
            st.subheader("🏷️ Trending Hashtags:")
            st.code(f"#{topic.replace(' ', '')} #ViralReels #Creator2026 #{platform.replace(' ', '')} #Trending")
        else:
            st.warning("कृपया कोई Topic लिखें।")

# ----------------- TAB 2: IMAGE CONVERTER & RESIZER -----------------
with tab2:
    st.header("🖼️ Image Converter & Resizer")
    st.write("इमेज का साइज़ कम करें और फ़ॉर्मेट बदलें!")
    
    uploaded_file = st.file_uploader("अपनी फोटो अपलोड करें:", type=["jpg", "jpeg", "png", "webp"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        format_choice = st.selectbox("किस फ़ॉर्मेट में कन्वर्ट करना है?", ["PNG", "JPEG", "WEBP"])
        quality_val = st.slider("Quality/Compression (100 = Best Quality, 50 = Smaller Size):", 10, 100, 85)
        
        if st.button("⚡ Convert & Compress"):
            buffer = io.BytesIO()
            if format_choice == "JPEG":
                image.convert("RGB").save(buffer, format="JPEG", quality=quality_val)
                mime_type = "image/jpeg"
                ext = "jpg"
            elif format_choice == "WEBP":
                image.save(buffer, format="WEBP", quality=quality_val)
                mime_type = "image/webp"
                ext = "webp"
            else:
                image.save(buffer, format="PNG")
                mime_type = "image/png"
                ext = "png"
                
            buffer.seek(0)
            st.success("इमेज तैयार है! नीचे से डाउनलोड करें:")
            st.download_button(label=f"📥 Download .{ext} Image", data=buffer, file_name=f"converted_image.{ext}", mime=mime_type)

# ----------------- TAB 3: PRO PROMPT ENHANCER -----------------
with tab3:
    st.header("🎨 Pro AI Prompt Enhancer")
    st.write("साधारण प्रॉम्ट को ChatGPT, Midjourney और Sora के लिए 8K HD प्रॉम्ट में बदलें!")
    
    simple_prompt = st.text_input("साधारण प्रॉम्ट लिखें (e.g., A cat in space):")
    style = st.selectbox("Style चुनें:", ["Cyberpunk / Futuristic", "Cinematic 8K Photorealistic", "3D Pixar Animation", "Anime / Manga"])
    
    if st.button("🚀 Enhance Prompt"):
        if simple_prompt.strip() != "":
            enhanced = f"{simple_prompt}, {style} style, ultra-detailed 8k resolution, volumetric lighting, photorealistic depth of field, masterpiece, highly intricate, Unreal Engine 5 render"
            st.subheader("🔥 आपका Pro AI Prompt:")
            st.code(enhanced, language="text")
            st.success("इसे कॉपी करके ChatGPT, Midjourney या AI Image Tools में पेस्ट करें!")
        else:
            st.warning("कृपया प्रॉम्ट लिखें।")
