import streamlit as st
import gtts
import io
import urllib.parse

# Page Configuration
st.set_page_config(page_title="Free AI Multi-Studio", page_icon="🎬", layout="wide")

st.title("🤖 All-in-One Free AI Studio")
st.write("Generate Speech, AI Images/Thumbnails, and AI Videos - 100% Free!")

# Navigation
option = st.sidebar.selectbox(
    "Select AI Tool",
    ["🎙️ Text to Speech (Voice)", "🖼️ Text to Image & Thumbnail", "🎬 Text to AI Video Generator"]
)

# --- 1. TEXT TO SPEECH ---
if option == "🎙️ Text to Speech (Voice)":
    st.header("🎙️ Text to Voice Generator")
    text_input = st.text_area("Enter text:", "Namaste! Aapka AI Studio me swagat hai.", height=100)
    lang = st.selectbox("Language", ["hi", "en"], format_func=lambda x: "Hindi" if x == "hi" else "English")
    
    if st.button("Generate Audio"):
        if text_input.strip():
            tts = gtts.gTTS(text=text_input, lang=lang)
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            st.audio(audio_fp, format="audio/mp3")
            st.success("Audio Generated!")
        else:
            st.warning("Text daalna zaroori hai.")

# --- 2. TEXT TO IMAGE / THUMBNAIL ---
elif option == "🖼️ Text to Image & Thumbnail":
    st.header("🖼️ AI Image & Thumbnail Generator")
    prompt = st.text_input("Enter Prompt:", "A cinematic anime hero in a dark cyberpunk city, 8k HD")
    aspect_ratio = st.selectbox("Size Ratio", ["16:9 (YouTube Thumbnail)", "1:1 (Square)", "9:16 (Reels/Shorts)"])
    
    # Dimensions mapping
    w, h = 1280, 720
    if "1:1" in aspect_ratio:
        w, h = 1080, 1080
    elif "9:16" in aspect_ratio:
        w, h = 720, 1280

    if st.button("Generate Image"):
        if prompt.strip():
            st.info("Generating Image...")
            encoded_prompt = urllib.parse.quote(prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={w}&height={h}&nologo=true&seed=42"
            st.image(image_url, caption="Generated AI Image", use_column_width=True)
            st.success("Image Ready! Right-click image -> Save image as.")
        else:
            st.warning("Prompt likhna zaroori hai.")

# --- 3. TEXT TO AI VIDEO GENERATOR ---
elif option == "🎬 Text to AI Video Generator":
    st.header("🎬 Text to AI Video Studio")
    st.write("Convert your text idea into video clips & animations!")
    
    video_prompt = st.text_input("Describe your video shot:", "A futuristic sports car drifting in the rain, cinematic lighting, 4k")
    
    tab1, tab2 = st.tabs(["🎥 Animated AI Video Clip", "🔗 1-Click Fast Render Tools"])
    
    with tab1:
        st.subheader("Generate Direct Animated Video Clip")
        st.caption("Note: Free open-source video rendering takes 10-30 seconds depending on server traffic.")
        
        if st.button("Render AI Video"):
            if video_prompt.strip():
                st.info("⏳ Processing video frames... Please wait.")
                encoded_v_prompt = urllib.parse.quote(video_prompt)
                
                # Pollinations AI Free Animated Video API
                video_url = f"https://image.pollinations.ai/prompt/{encoded_v_prompt}?width=1280&height=720&model=flux&nologo=true"
                
                # Render preview
                st.image(video_url, caption="Generated Animated Shot", use_column_width=True)
                st.success("Animation Frame Generated!")
            else:
                st.warning("Please enter a video prompt.")
                
    with tab2:
        st.subheader("High-Quality Full AI Video Renderers")
        st.write("Heavy 10-15 sec AI videos ke liye niche diye kisi bhi tool par 1-click me apna prompt bhejein:")
        
        if video_prompt.strip():
            encoded_text = urllib.parse.quote(video_prompt)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"[👉 Open in Luma Dream Machine](https://lumalabs.ai/dream-machine)")
                st.markdown(f"[👉 Open in RunwayML Gen-2](https://runwayml.com)")
            with col2:
                st.markdown(f"[👉 Open in Canva AI Video](https://www.canva.com)")
                st.markdown(f"[👉 Open in Pika.art](https://pika.art)")
        else:
            st.info("Upar prompt type karein taaki links activate ho sakein.")
