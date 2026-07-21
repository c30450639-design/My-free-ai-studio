import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import io
import urllib.parse
from gtts import gTTS
from fpdf import FPDF

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="StudioX Pro 2026 | Global Enterprise AI Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# LUXURY ENTERPRISE CSS STYLING
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main {
        background: radial-gradient(circle at top right, #1e1b4b 0%, #0f172a 40%, #020617 100%);
        color: #f8fafc;
    }
    
    .brand-glow {
        text-align: center;
        padding: 20px 0 10px 0;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }
    
    .hero-subtitle {
        font-size: 1.15rem;
        color: #94a3b8;
        max-width: 700px;
        margin: 0 auto 1.8rem auto;
        line-height: 1.6;
    }
    
    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }

    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #06b6d4 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.5) !important;
        width: 100%;
        letter-spacing: 0.5px;
    }

    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 15px 35px -5px rgba(79, 70, 229, 0.7) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(15, 23, 42, 0.85);
        padding: 10px;
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        color: #94a3b8;
        font-weight: 600;
        padding: 10px 18px;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3) !important;
    }

    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background-color: rgba(15, 23, 42, 0.7) !important;
        color: #f8fafc !important;
    }

    .vip-badge {
        background: linear-gradient(90deg, #f43f5e, #fb7185);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# GLOBAL MULTILINGUAL VOICE DICTATION WIDGET
# ---------------------------------------------------------
LANGUAGES = {
    "English (US)": "en-US",
    "Hindi (हिंदी)": "hi-IN",
    "Spanish (Español)": "es-ES",
    "French (Français)": "fr-FR",
    "German (Deutsch)": "de-DE",
    "Japanese (日本語)": "ja-JP",
    "Chinese (Mandarin)": "zh-CN",
    "Arabic (العربية)": "ar-SA",
    "Russian (Русский)": "ru-RU",
    "Portuguese (Português)": "pt-BR",
    "Bengali (বাংলা)": "bn-IN",
    "Marathi (मराठी)": "mr-IN",
    "Telugu (తెలుగు)": "te-IN",
    "Tamil (தமிழ்)": "ta-IN",
    "Gujarati (ગુજરાતી)": "gu-IN",
    "Kannada (ಕನ್ನಡ)": "kn-IN",
    "Malayalam (മലയാളം)": "ml-IN",
    "Punjabi (ਪੰਜਾਬੀ)": "pa-IN",
    "Urdu (اردو)": "ur-PK"
}

def voice_typing_widget(box_label):
    st.markdown(f"##### 🎙️ Voice Dictation ({box_label})")
    selected_lang = st.selectbox(
        f"Select Voice Language for {box_label}:",
        options=list(LANGUAGES.keys()),
        key=f"lang_select_{box_label.replace(' ', '_')}"
    )
    lang_code = LANGUAGES[selected_lang]

    mic_html = f"""
    <div style="background: rgba(30, 41, 59, 0.6); padding: 12px 16px; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
        <div>
            <span style="color:#38bdf8; font-size:13px; font-weight:700;">🎤 Active Language: {selected_lang}</span>
            <p id="speech_output_{box_label.replace(' ', '_')}" style="color:#a7f3d0; font-size:12px; margin: 4px 0 0 0; font-weight:600;"></p>
        </div>
        <div>
            <button onclick="startDictation('{lang_code}')" style="background: linear-gradient(135deg, #059669, #10b981); color:white; border:none; padding:8px 16px; border-radius:10px; cursor:pointer; font-size:12px; font-weight:700; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);">🎙️ Click to Speak ({selected_lang.split()[0]})</button>
        </div>
    </div>

    <script>
    function startDictation(langCode) {{
        if (window.hasOwnProperty('webkitSpeechRecognition')) {{
            var recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = langCode;
            recognition.start();

            document.getElementById('speech_output_{box_label.replace(' ', '_')}').innerHTML = "🎤 Listening... Please speak now!";

            recognition.onresult = function(e) {{
                var transcript = e.results[0][0].transcript;
                document.getElementById('speech_output_{box_label.replace(' ', '_')}').innerHTML = "✅ Recorded: '" + transcript + "' (Copy & paste into the input field below)";
                recognition.stop();
            }};

            recognition.onerror = function(e) {{
                document.getElementById('speech_output_{box_label.replace(' ', '_')}').innerHTML = "⚠️ Speech not recognized. Please try speaking again.";
                recognition.stop();
            }}
        }} else {{
            alert("Your browser does not support Voice Dictation. Please use Google Chrome!");
        }}
    }}
    </script>
    """
    components.html(mic_html, height=80)

# Helper function for PDF
def create_pdf(title_text, content_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, title_text.encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(8)
    pdf.set_font("Helvetica", size=11)
    lines = content_text.split('\n')
    for line in lines:
        clean_line = line.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 7, clean_line)
    return pdf.output()

# SIDEBAR
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/lightning-bolt.png", width=60)
    st.title("⚡ StudioX Pro")
    st.caption("Global Edition v10.0 (2026)")
    st.markdown("---")
    
    st.markdown('<span class="vip-badge">GLOBAL ACTIVE</span>', unsafe_allow_html=True)
    st.success("🌐 20+ Languages Voice Input Supported")
    
    st.markdown("---")
    st.subheader("📢 Sponsored Section")
    adsterra_sidebar = """
    <div style="background: rgba(30, 41, 59, 0.5); padding: 12px; border-radius: 14px; text-align: center; border: 1px dashed rgba(255, 255, 255, 0.15);">
        <span style="color:#94a3b8; font-size:11px; letter-spacing:1px; font-weight:700;">ADVERTISEMENT</span><br/>
        <a href="#" style="color:#38bdf8; text-decoration:none; font-size:13px; font-weight:bold; display:block; margin-top:6px;">🚀 Scale Your Viral Traffic Today</a>
    </div>
    """
    components.html(adsterra_sidebar, height=100)

# HERO SECTION
st.markdown("""
<div class="brand-glow">
    <div class="hero-title">StudioX Pro Global Enterprise</div>
    <div class="hero-subtitle">World's First Multilingual AI Suite — Speak in 20+ Languages to Generate Apps, PDF Documents, Web Code & Visuals</div>
</div>
""", unsafe_allow_html=True)

# TOP BANNER AD
top_ad = """
<div style="text-align:center; margin-bottom: 20px;">
    <div style="background: rgba(30, 41, 59, 0.4); padding: 10px; border-radius: 12px; border: 1px dashed rgba(255, 255, 255, 0.12); display: inline-block; width: 100%; max-width: 728px;">
        <span style="color:#64748b; font-size:11px; font-weight:700; letter-spacing:1px;">SPONSORED ADVERTISEMENT SLOT</span>
    </div>
</div>
"""
components.html(top_ad, height=55)

# MAIN TABS
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📄 PDF Creator",
    "📱 Mobile App Builder", 
    "💻 Web Code Builder", 
    "🎬 AI Animation Suite",
    "📸 Social Viral Scripts",
    "🖼️ HD Studio & Icons", 
    "🎙️ Voiceover Engine"
])

# TAB 1: PDF CREATOR
with tab1:
    st.markdown('<span class="vip-badge">PDF SUITE</span>', unsafe_allow_html=True)
    st.markdown("### 📄 Ultra Fast Multilingual PDF Generator")
    voice_typing_widget("PDF Content")
    
    pdf_title = st.text_input("📌 PDF Document Heading/Title:", placeholder="e.g., Global AI Strategy Document")
    pdf_body = st.text_area("📝 Document Content (Text or Code):", height=180, placeholder="Write or speak in any language to generate PDF...")
    
    if st.button("🚀 Generate PDF Document", key="btn_pdf"):
        if pdf_title.strip() != "" and pdf_body.strip() != "":
            try:
                pdf_bytes = create_pdf(pdf_title, pdf_body)
                st.success("✅ PDF File Successfully Created!")
                st.download_button(
                    label="📥 Download PDF File Now",
                    data=bytes(pdf_bytes),
                    file_name=f"{pdf_title.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
        else:
            st.warning("⚠️ Please fill both Title and Content fields.")

# TAB 2: MOBILE APP BUILDER
with tab2:
    st.markdown('<span class="vip-badge">APP BUILDER</span>', unsafe_allow_html=True)
    st.markdown("### 📱 Flutter Mobile App Code Generator")
    voice_typing_widget("App Concept")
    
    app_name = st.text_input("🎯 App Concept / Name:", placeholder="e.g., Multi-language Cloud Storage App")
    if st.button("🚀 Generate App Code", key="btn_app"):
        if app_name.strip() != "":
            st.success("✅ Flutter App Code Generated!")
            code = f"""// Complete Flutter App Code for: {app_name}
import 'package:flutter/material.dart';

void main() {{
  runApp(const MyApp());
}}

class MyApp extends StatelessWidget {{
  const MyApp({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: '{app_name}',
      theme: ThemeData.dark(),
      home: Scaffold(
        appBar: AppBar(title: Text('{app_name}')),
        body: Center(child: Text('Welcome to {app_name}')),
      ),
    );
  }}
}}"""
            st.code(code, language="dart")
        else:
            st.warning("⚠️ Please describe your app concept.")

# TAB 3: WEB CODE BUILDER
with tab3:
    st.markdown('<span class="vip-badge">WEB BUILDER</span>', unsafe_allow_html=True)
    st.markdown("### 💻 HTML / CSS & Web UI Generator")
    voice_typing_widget("Web Requirement")
    
    web_req = st.text_input("🎯 Web Design Goal:", placeholder="e.g., Responsive landing page form")
    if st.button("🚀 Generate Web Code", key="btn_web"):
        if web_req.strip() != "":
            st.code(f"<!-- {web_req} -->\n<div class='glass-card'><h1>{web_req}</h1><button>Submit</button></div>", language="html")

# TAB 4: AI ANIMATION SUITE
with tab4:
    st.markdown('<span class="vip-badge">ANIMATION SUITE</span>', unsafe_allow_html=True)
    st.markdown("### 🎬 Video & Animation Prompts Engine")
    voice_typing_widget("Animation Story")
    
    anim_req = st.text_input("🎯 Scene Story / Anime Concept:", placeholder="e.g., Cyberpunk city scene")
    if st.button("🚀 Generate Scene Prompts", key="btn_anim"):
        if anim_req.strip() != "":
            st.code(f"SCENE 1: Cinematic shot of {anim_req}, 8k anime style, 60fps.\nSCENE 2: Slow motion action sequence.", language="text")

# TAB 5: SOCIAL VIRAL SCRIPTS
with tab5:
    st.markdown('<span class="vip-badge">VIRAL SOCIAL</span>', unsafe_allow_html=True)
    st.markdown("### 📸 Social Script Generator")
    voice_typing_widget("Social Topic")
    
    soc_topic = st.text_input("🎯 Video / Reel Topic:", placeholder="e.g., Top 5 AI tools in 2026")
    if st.button("🚀 Generate Script", key="btn_soc"):
        if soc_topic.strip() != "":
            st.code(f"Hook: Stop scrolling! Want to learn about {soc_topic}?\nCaption: Exploring AI in 2026! #{soc_topic.replace(' ','')}", language="text")

# TAB 6: HD STUDIO & ICONS
with tab6:
    st.markdown('<span class="vip-badge">IMAGE STUDIO</span>', unsafe_allow_html=True)
    st.markdown("### 🖼️ AI App Icon & Thumbnail Generator")
    voice_typing_widget("Icon Prompt")
    
    img_prompt = st.text_input("🎨 Image Prompt (English works best):", "Modern 3D app icon, neon isometric style, 4k quality")
    if st.button("✨ Generate HD Visual", key="btn_img"):
        if img_prompt.strip() != "":
            encoded = urllib.parse.quote(img_prompt)
            st.image(f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true", use_column_width=True)

# TAB 7: VOICEOVER ENGINE
with tab7:
    st.markdown('<span class="vip-badge">VOICE SUITE</span>', unsafe_allow_html=True)
    st.markdown("### 🎙️ Text-to-Speech Audio Engine")
    voice_text = st.text_area("📝 Text to Voice:", "Welcome to StudioX Pro Global AI Studio.", height=90)
    if st.button("🔊 Generate Audio Voiceover", key="btn_voice"):
        if voice_text.strip() != "":
            tts = gTTS(text=voice_text, lang="en")
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format="audio/mp3")

# FOOTER
st.markdown("---")
bottom_ad = """
<div style="text-align:center; padding: 10px;">
    <p style="color:#64748b; font-size:12px; font-weight:600;">© 2026 StudioX Pro Global | Multilingual AI Suite</p>
</div>
"""
components.html(bottom_ad, height=50)
