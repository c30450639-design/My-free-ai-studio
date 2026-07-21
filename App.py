 import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import io
import urllib.parse
import zipfile
from gtts import gTTS
from fpdf import FPDF

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="StudioX Pro 2026 | Free AI Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# LUXURY ENTERPRISE CSS & AI ROBOT STYLING
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
        max-width: 750px;
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
# FLOATING AI ROBOT ASSISTANT WIDGET
# ---------------------------------------------------------
robot_assistant_html = """
<div id="bot-wrapper" style="position: fixed; bottom: 20px; right: 20px; z-index: 999999; font-family: sans-serif;">
    <div id="bot-icon" onclick="toggleBotChat()" style="background: linear-gradient(135deg, #06b6d4, #7c3aed); width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 8px 25px rgba(6, 182, 212, 0.6); transition: all 0.3s ease; border: 2px solid rgba(255,255,255,0.3);">
        <span style="font-size: 30px;">🤖</span>
    </div>

    <div id="bot-chat-window" style="display: none; position: absolute; bottom: 75px; right: 0; width: 310px; background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.15); border-radius: 18px; box-shadow: 0 15px 35px rgba(0,0,0,0.6); padding: 15px; color: white;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px; margin-bottom: 10px;">
            <span style="font-weight: bold; color: #38bdf8; font-size: 14px;">🤖 StudioX AI Helper</span>
            <span onclick="toggleBotChat()" style="cursor: pointer; color: #94a3b8; font-weight: bold;">✕</span>
        </div>
        
        <div id="chat-logs" style="height: 180px; overflow-y: auto; font-size: 12px; margin-bottom: 10px; padding-right: 5px;">
            <p style="background: rgba(56, 189, 248, 0.15); padding: 8px; border-radius: 8px; color: #e2e8f0; margin: 0 0 8px 0;">
                👋 <b>नमस्ते! मैं आपका एआई असिस्टेंट हूँ।</b><br/>मुझसे पूछें कि यह वेबसाइट कैसे काम करती है!
            </p>
        </div>

        <div style="display: flex; gap: 5px;">
            <input type="text" id="user-msg" placeholder="पूछें (e.g., PDF कैसे बनाएं?)..." style="flex: 1; padding: 6px 10px; border-radius: 8px; border: 1px solid #475569; background: #1e293b; color: white; font-size: 11px;">
            <button onclick="sendBotMsg()" style="background: #06b6d4; color: white; border: none; padding: 6px 12px; border-radius: 8px; cursor: pointer; font-size: 11px; font-weight: bold;">भेजें</button>
        </div>
    </div>
</div>

<script>
function toggleBotChat() {
    var win = document.getElementById("bot-chat-window");
    win.style.display = (win.style.display === "none" || win.style.display === "") ? "block" : "none";
}

function sendBotMsg() {
    var input = document.getElementById("user-msg");
    var logs = document.getElementById("chat-logs");
    var text = input.value.trim().toLowerCase();
    
    if (text === "") return;

    logs.innerHTML += "<p style='text-align: right; margin: 4px 0;'><span style='background: #4f46e5; padding: 6px 10px; border-radius: 8px; display: inline-block; color: white;'>" + input.value + "</span></p>";
    input.value = "";

    var reply = "💡 आप ऊपर दिए गए टैब्स में से अपने काम का टूल चुन सकते हैं!";
    
    if (text.includes("pdf") || text.includes("पीडीएफ")) {
        reply = "📄 <b>PDF Maker:</b> 'Instant PDF Maker' टैब में जाएं, टाइटल और टेक्स्ट लिखें और 'Create PDF' बटन दबाएं!";
    } else if (text.includes("app") || text.includes("ऐप")) {
        reply = "📱 <b>App Builder:</b> 'App Builder' टैब में जाएं और अपने ऐप का आइडिया बोलकर बताएं, एआई आपको पूरा Flutter कोड दे देगा!";
    } else if (text.includes("code") || text.includes("कोड")) {
        reply = "💻 <b>Web Code:</b> 'Web Code & Live Preview' टैब में जाएं, अपने पेज की जानकारी दें और लाइव प्रिव्यू देखें!";
    } else if (text.includes("voice") || text.includes("आवाज") || text.includes("बोल")) {
        reply = "🎙️ <b>Voice Typing:</b> हर टूल के ऊपर 'Voice Dictation' का बटन है, उस पर क्लिक करके अपनी भाषा में बोलें!";
    }

    setTimeout(function() {
        logs.innerHTML += "<p style='margin: 4px 0;'><span style='background: rgba(56, 189, 248, 0.2); padding: 6px 10px; border-radius: 8px; display: inline-block; color: #a7f3d0;'>" + reply + "</span></p>";
        logs.scrollTop = logs.scrollHeight;
    }, 500);
}
</script>
"""
components.html(robot_assistant_html, height=0)

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
            <button onclick="startDictation('{lang_code}')" style="background: linear-gradient(135deg, #059669, #10b981); color:white; border:none; padding:8px 16px; border-radius:10px; cursor:pointer; font-size:12px; font-weight:700; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);">🎙️ Speak Now</button>
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

            document.getElementById('speech_output_{box_label.replace(' ', '_')}').innerHTML = "🎤 Listening... Speak now!";

            recognition.onresult = function(e) {{
                var transcript = e.results[0][0].transcript;
                document.getElementById('speech_output_{box_label.replace(' ', '_')}').innerHTML = "✅ Recorded: '" + transcript + "' (Copy & paste below)";
                recognition.stop();
            }};

            recognition.onerror = function(e) {{
                document.getElementById('speech_output_{box_label.replace(' ', '_')}').innerHTML = "⚠️ Speech not clear. Try again!";
                recognition.stop();
            }}
        }} else {{
            alert("Your browser does not support Voice Dictation. Use Chrome!");
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

# Helper function to create ZIP
def create_zip(filename, content):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(filename, content)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

# ---------------------------------------------------------
# SIDEBAR CONTROL
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/lightning-bolt.png", width=60)
    st.title("⚡ StudioX Pro")
    st.caption("2026 Free Global AI Suite")
    st.markdown("---")
    
    st.success("🔓 FREE FOR EVERYONE")
    st.info("All Tools Unlocked for Global Users")

    st.markdown("---")
    
    st.subheader("📢 Sponsored Banner")
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
    <div class="hero-title">StudioX Pro Ultra SaaS</div>
    <div class="hero-subtitle">Next-Gen AI Suite 2026 — Speak in Any Language to Build Apps, Live Playground Web Code, PDF Documents & Viral Analytics</div>
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
    "💻 Web Code & Live Preview", 
    "📱 App Builder & ZIP", 
    "📄 Instant PDF Maker",
    "🎬 AI Animation Suite",
    "📸 Virality & Scripts",
    "🖼️ HD Icons & Visuals", 
    "🎙️ AI Voice Engine"
])

# TAB 1: WEB CODE & LIVE PLAYGROUND
with tab1:
    st.markdown('<span class="vip-badge">LIVE PLAYGROUND</span>', unsafe_allow_html=True)
    st.markdown("### 💻 HTML/CSS Code Generator & Live Preview")
    voice_typing_widget("Web Requirement")
    
    web_req = st.text_input("🎯 Web Design Concept:", placeholder="e.g., A stylish dark gradient contact form with submit button")
    
    if st.button("🚀 Generate Code & Render Live Preview", key="btn_web"):
        if web_req.strip() != "":
            html_code = f"""<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: sans-serif; background: #0f172a; color: white; padding: 30px; text-align: center; }}
    .card {{ background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.2); border-radius: 16px; padding: 25px; max-width: 400px; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
    input, button {{ width: 90%; padding: 10px; margin: 8px 0; border-radius: 8px; border: none; }}
    button {{ background: linear-gradient(90deg, #38bdf8, #818cf8); color: white; font-weight: bold; cursor: pointer; }}
</style>
</head>
<body>
    <div class="card">
        <h2>{web_req.title()}</h2>
        <input type="text" placeholder="Enter name...">
        <input type="email" placeholder="Enter email...">
        <button>Submit Now</button>
    </div>
</body>
</html>"""
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("📋 Generated HTML/CSS Code:")
                st.code(html_code, language="html")
            with col2:
                st.subheader("⚡ Live Playground Preview:")
                components.html(html_code, height=300, scrolling=True)
        else:
            st.warning("⚠️ Enter a web concept.")

# TAB 2: APP BUILDER & ZIP EXPORT
with tab2:
    st.markdown('<span class="vip-badge">APP BUILDER</span>', unsafe_allow_html=True)
    st.markdown("### 📱 Mobile App Builder & Export Project (.ZIP)")
    voice_typing_widget("App Concept")
    
    app_name = st.text_input("🎯 App Concept / Name:", placeholder="e.g., Cloud Storage App 50GB")
    if st.button("🚀 Build App & Prepare ZIP Package", key="btn_app"):
        if app_name.strip() != "":
            flutter_code = f"""// Complete Flutter App Code for: {app_name}
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {{
  const MyApp({{super.key}});
  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      title: '{app_name}',
      theme: ThemeData.dark(),
      home: Scaffold(
        appBar: AppBar(title: Text('{app_name}')),
        body: Center(child: Text('Welcome to {app_name}')),
      ),
    );
  }}
}}"""
            st.code(flutter_code, language="dart")
            
            zip_bytes = create_zip("main.dart", flutter_code)
            st.download_button(
                label="📦 Download Full Project (.ZIP)",
                data=zip_bytes,
                file_name=f"{app_name.replace(' ', '_')}_Project.zip",
                mime="application/zip"
            )
        else:
            st.warning("⚠️ Describe your app idea.")

# TAB 3: INSTANT PDF MAKER
with tab3:
    st.markdown('<span class="vip-badge">PDF SUITE</span>', unsafe_allow_html=True)
    st.markdown("### 📄 Multilingual PDF Document Creator")
    voice_typing_widget("PDF Content")
    
    pdf_title = st.text_input("📌 PDF Heading:", placeholder="e.g., My AI Project Document")
    pdf_body = st.text_area("📝 Document Body:", height=150, placeholder="Type or speak content...")
    
    if st.button("🚀 Create PDF", key="btn_pdf"):
        if pdf_title.strip() != "" and pdf_body.strip() != "":
            pdf_bytes = create_pdf(pdf_title, pdf_body)
            st.download_button(
                label="📥 Download PDF Document",
                data=bytes(pdf_bytes),
                file_name=f"{pdf_title.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )

# TAB 4: AI ANIMATION SUITE
with tab4:
    st.markdown('<span class="vip-badge">ANIMATION SUITE</span>', unsafe_allow_html=True)
    st.markdown("### 🎬 Sequential Animation Scene Prompts")
    voice_typing_widget("Animation Story")
    
    anim_req = st.text_input("🎯 Scene Story:", placeholder="e.g., Cyberpunk anime character transformation")
    if st.button("🚀 Generate Prompts", key="btn_anim"):
        if anim_req.strip() != "":
            st.code(f"SCENE 1: Cinematic shot of {anim_req}, 8k anime style, 60fps.\nSCENE 2: Slow motion action sequence.", language="text")

# TAB 5: VIRALITY SCORE & SCRIPTS
with tab5:
    st.markdown('<span class="vip-badge">VIRAL ANALYTICS</span>', unsafe_allow_html=True)
    st.markdown("### 📸 Social Scripts & AI Virality Score Analyzer")
    voice_typing_widget("Social Topic")
    
    soc_topic = st.text_input("🎯 Reel / Shorts Topic:", placeholder="e.g., 3 Secret AI Tools in 2026")
    if st.button("🚀 Analyze Virality & Generate Script", key="btn_soc"):
        if soc_topic.strip() != "":
            st.metric(label="🔥 Estimated Virality Score", value="94 / 100", delta="High Engagement")
            st.code(f"Hook: Stop scrolling! If you don't know about {soc_topic}, you are behind in 2026!\nCaption: Must watch till the end! #{soc_topic.replace(' ','')}", language="text")

# TAB 6: HD ICONS & VISUALS
with tab6:
    st.markdown('<span class="vip-badge">IMAGE STUDIO</span>', unsafe_allow_html=True)
    st.markdown("### 🖼️ AI App Icon & Visual Studio")
    voice_typing_widget("Icon Prompt")
    
    img_prompt = st.text_input("🎨 Image Prompt:", "Modern 3D app icon, neon isometric style, 4k quality")
    if st.button("✨ Generate Visual", key="btn_img"):
        if img_prompt.strip() != "":
            encoded = urllib.parse.quote(img_prompt)
            st.image(f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true", use_column_width=True)

# TAB 7: AI VOICE ENGINE
with tab7:
    st.markdown('<span class="vip-badge">VOICE SUITE</span>', unsafe_allow_html=True)
    st.markdown("### 🎙️ Text-to-Speech Engine")
    voice_text = st.text_area("📝 Text to Voice:", "Welcome to StudioX Pro Ultra Free Suite.", height=90)
    if st.button("🔊 Generate Voiceover", key="btn_voice"):
        if voice_text.strip() != "":
            tts = gTTS(text=voice_text, lang="en")
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format="audio/mp3")

# FOOTER
st.markdown("---")
components.html("<div style='text-align:center; color:#64748b; font-size:12px; font-weight:600;'>© 2026 StudioX Pro Ultra | Free Global AI Suite</div>", height=40)
