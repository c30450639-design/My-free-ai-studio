import streamlit as st
import streamlit.components.v1 as components
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
# LUXURY ENTERPRISE CSS
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
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        color: #94a3b8;
        font-weight: 600;
        padding: 10px 18px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%) !important;
        color: #ffffff !important;
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
# DRAGGABLE & VOICE-ENABLED SMALL ROBOT ASSISTANT WIDGET
# ---------------------------------------------------------
robot_assistant_html = """
<style>
    #draggable-bot {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 999999;
        font-family: 'Plus Jakarta Sans', sans-serif;
        cursor: grab;
        user-select: none;
    }
    #draggable-bot:active {
        cursor: grabbing;
    }
    .mini-bot-icon {
        background: linear-gradient(135deg, #06b6d4, #7c3aed);
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 6px 20px rgba(6, 182, 212, 0.6);
        border: 2px solid rgba(255,255,255,0.4);
        font-size: 24px;
        transition: transform 0.2s ease;
    }
    .mini-bot-icon:hover {
        transform: scale(1.1);
    }
    .bot-chat-box {
        display: none;
        position: absolute;
        bottom: 60px;
        right: 0;
        width: 300px;
        background: #0f172a;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 16px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.8);
        padding: 14px;
        color: white;
        cursor: default;
    }
</style>

<div id="draggable-bot">
    <div class="mini-bot-icon" onclick="toggleBotChat()" title="पकड़कर कहीं भी खींचें">🤖</div>

    <div id="bot-chat-window" class="bot-chat-box">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 6px; margin-bottom: 8px;">
            <span style="font-weight: bold; color: #38bdf8; font-size: 13px;">🤖 AI Robot (पकड़कर घुमाएं)</span>
            <span onclick="toggleBotChat()" style="cursor: pointer; color: #94a3b8; font-weight: bold;">✕</span>
        </div>
        
        <div id="chat-logs" style="height: 160px; overflow-y: auto; font-size: 12px; margin-bottom: 8px; padding-right: 4px;">
            <p style="background: rgba(56, 189, 248, 0.15); padding: 7px; border-radius: 8px; color: #e2e8f0; margin: 0 0 6px 0;">
                👋 <b>नमस्ते!</b> मुझे पकड़कर स्क्रीन पर कहीं भी ले जा सकते हैं। टाइप करें या नीचे माइक दबाकर बोलें!
            </p>
        </div>

        <div style="display: flex; gap: 4px; margin-bottom: 6px;">
            <input type="text" id="user-msg" placeholder="सवाल पूछें..." style="flex: 1; padding: 6px 8px; border-radius: 6px; border: 1px solid #475569; background: #1e293b; color: white; font-size: 11px;">
            <button onclick="sendBotMsg()" style="background: #06b6d4; color: white; border: none; padding: 6px 10px; border-radius: 6px; cursor: pointer; font-size: 11px; font-weight: bold;">भेजें</button>
        </div>
        <button onclick="startRobotVoice()" style="width: 100%; background: linear-gradient(135deg, #059669, #10b981); color: white; border: none; padding: 6px; border-radius: 6px; cursor: pointer; font-size: 11px; font-weight: bold;">🎤 बोलकर पूछें (Voice Input)</button>
    </div>
</div>

<script>
// DRAG AND DROP LOGIC FOR ROBOT
const botEl = document.getElementById("draggable-bot");
let isDragging = false;
let offsetX, offsetY;

botEl.addEventListener("mousedown", (e) => {
    // Only drag if clicking the bot icon, not inside chat box
    if(e.target.closest('.bot-chat-box')) return;
    isDragging = true;
    offsetX = e.clientX - botEl.getBoundingClientRect().left;
    offsetY = e.clientY - botEl.getBoundingClientRect().top;
    botEl.style.cursor = "grabbing";
});

document.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    botEl.style.left = (e.clientX - offsetX) + "px";
    botEl.style.top = (e.clientY - offsetY) + "px";
    botEl.style.bottom = "auto";
    botEl.style.right = "auto";
});

document.addEventListener("mouseup", () => {
    isDragging = false;
    botEl.style.cursor = "grab";
});

// TOUCH SUPPORT FOR MOBILE DRAGGING
botEl.addEventListener("touchstart", (e) => {
    if(e.target.closest('.bot-chat-box')) return;
    isDragging = true;
    offsetX = e.touches[0].clientX - botEl.getBoundingClientRect().left;
    offsetY = e.touches[0].clientY - botEl.getBoundingClientRect().top;
});

document.addEventListener("touchmove", (e) => {
    if (!isDragging) return;
    botEl.style.left = (e.touches[0].clientX - offsetX) + "px";
    botEl.style.top = (e.touches[0].clientY - offsetY) + "px";
    botEl.style.bottom = "auto";
    botEl.style.right = "auto";
}, { passive: true });

document.addEventListener("touchend", () => {
    isDragging = false;
});

// CHAT TOGGLE & BOT RESPONSES
function toggleBotChat() {
    var win = document.getElementById("bot-chat-window");
    win.style.display = (win.style.display === "none" || win.style.display === "") ? "block" : "none";
}

function processQuery(text) {
    var logs = document.getElementById("chat-logs");
    logs.innerHTML += "<p style='text-align: right; margin: 4px 0;'><span style='background: #4f46e5; padding: 5px 8px; border-radius: 6px; display: inline-block; color: white;'>" + text + "</span></p>";
    
    var reply = "💡 आप ऊपर दिए गए टैब्स का उपयोग कर सकते हैं!";
    var lowerText = text.toLowerCase();
    
    if (lowerText.includes("qr") || lowerText.includes("क्यूआर")) {
        reply = "📲 <b>QR Generator:</b> पहले टैब 'Social QR Generator' में जाकर अपने चैनल का लिंक या नाम डालें!";
    } else if (lowerText.includes("pdf") || lowerText.includes("पीडीएफ")) {
        reply = "📄 <b>PDF Maker:</b> 'Instant PDF Maker' टैब में जाकर टेक्स्ट लिखें और PDF डाउनलोड करें!";
    } else if (lowerText.includes("app") || lowerText.includes("ऐप")) {
        reply = "📱 <b>App Builder:</b> 'Mobile App Builder' टैब में अपने ऐप का आइडिया लिखें!";
    }

    setTimeout(function() {
        logs.innerHTML += "<p style='margin: 4px 0;'><span style='background: rgba(56, 189, 248, 0.2); padding: 5px 8px; border-radius: 6px; display: inline-block; color: #a7f3d0;'>" + reply + "</span></p>";
        logs.scrollTop = logs.scrollHeight;
    }, 400);
}

function sendBotMsg() {
    var input = document.getElementById("user-msg");
    var text = input.value.trim();
    if (text === "") return;
    input.value = "";
    processQuery(text);
}

function startRobotVoice() {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'hi-IN'; // Default Hindi/English voice support
        recognition.start();

        var logs = document.getElementById("chat-logs");
        logs.innerHTML += "<p style='color: #f43f5e; font-size:11px; margin: 4px 0;'>🎤 सुन रहा हूँ, बोलिए...</p>";

        recognition.onresult = function(e) {
            var transcript = e.results[0][0].transcript;
            processQuery(transcript);
            recognition.stop();
        };

        recognition.onerror = function(e) {
            recognition.stop();
        }
    } else {
        alert("आपका ब्राउज़र वॉइस रिकग्निशन सपोर्ट नहीं करता। Chrome इस्तेमाल करें!");
    }
}
</script>
"""
components.html(robot_assistant_html, height=400)

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
    "Bengali (বাংলা)": "bn-IN",
    "Marathi (मराठी)": "mr-IN",
    "Telugu (తెలుగు)": "te-IN",
    "Tamil (தமிழ்)": "ta-IN",
    "Gujarati (ગુજરાતી)": "gu-IN",
    "Punjabi (ਪੰਜਾਬੀ)": "pa-IN"
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
                document.getElementById('speech_output_{box_label.replace(' ', '_')}').innerHTML = "✅ Recorded: '" + transcript + "'";
                recognition.stop();
            }};

            recognition.onerror = function(e) {{
                document.getElementById('speech_output_{box_label.replace(' ', '_')}').innerHTML = "⚠️ Try speaking again!";
                recognition.stop();
            }}
        }} else {{
            alert("Use Google Chrome for Voice Dictation!");
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

# Helper function for ZIP
def create_zip(filename, content):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(filename, content)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/lightning-bolt.png", width=60)
    st.title("⚡ StudioX Pro")
    st.caption("2026 Free Global AI Suite")
    st.markdown("---")
    st.success("🔓 ALL 8 TOOLS UNLOCKED")
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
    <div class="hero-subtitle">Next-Gen AI Suite 2026 — Generate Social QR Codes, Build Apps, Live Web Playground & PDF Documents</div>
</div>
""", unsafe_allow_html=True)

# TOP AD
top_ad = """
<div style="text-align:center; margin-bottom: 20px;">
    <div style="background: rgba(30, 41, 59, 0.4); padding: 10px; border-radius: 12px; border: 1px dashed rgba(255, 255, 255, 0.12); display: inline-block; width: 100%; max-width: 728px;">
        <span style="color:#64748b; font-size:11px; font-weight:700; letter-spacing:1px;">SPONSORED ADVERTISEMENT SLOT</span>
    </div>
</div>
"""
components.html(top_ad, height=55)

# MAIN TABS (8 CORE TOOLS)
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📲 Social QR Generator",
    "💻 Web Code Playground", 
    "📱 Mobile App Builder", 
    "📄 Instant PDF Maker",
    "🎬 AI Animation Suite",
    "📸 Virality & Scripts",
    "🖼️ HD Icons & Studio", 
    "🎙️ AI Voice Engine"
])

# =========================================================
# TAB 1: SOCIAL MEDIA QR CODE GENERATOR
# =========================================================
with tab1:
    st.markdown('<span class="vip-badge">QR STUDIO</span>', unsafe_allow_html=True)
    st.markdown("### 📲 Channel & Social Media Instant QR Generator")
    
    platform = st.selectbox("🌐 Select Platform:", [
        "YouTube Channel", "Instagram Profile", "Facebook Page", 
        "Telegram Channel", "WhatsApp Direct", "Custom Website URL"
    ])
    
    user_handle = st.text_input("🔗 Enter Channel Name / Username / URL:", placeholder="e.g., MyAwesomeChannel or https://youtube.com/@mychannel")
    
    if st.button("🚀 Generate HD Social QR Code", key="btn_qr"):
        if user_handle.strip() != "":
            final_url = user_handle
            if "YouTube" in platform and not user_handle.startswith("http"):
                final_url = f"https://youtube.com/@{user_handle.replace('@','')}"
            elif "Instagram" in platform and not user_handle.startswith("http"):
                final_url = f"https://instagram.com/{user_handle.replace('@','')}"
            elif "Facebook" in platform and not user_handle.startswith("http"):
                final_url = f"https://facebook.com/{user_handle}"
            elif "Telegram" in platform and not user_handle.startswith("http"):
                final_url = f"https://t.me/{user_handle.replace('@','')}"
            elif "WhatsApp" in platform and not user_handle.startswith("http"):
                final_url = f"https://wa.me/{user_handle.replace('+','').replace(' ','')}"
                
            encoded_url = urllib.parse.quote(final_url)
            qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_url}&color=38bdf8&bgcolor=0f172a"
            
            st.success(f"✅ HD QR Code Generated for: {final_url}")
            col_a, col_b = st.columns([1, 2])
            with col_a:
                st.image(qr_api, width=220, caption="Scan to Open Channel/Profile")
            with col_b:
                st.info(f"📍 **Target URL:** {final_url}")
                st.markdown(f"[📥 Click Here to Open/Download QR Image]({qr_api})")
        else:
            st.warning("⚠️ Please enter a username or channel link.")

# =========================================================
# TAB 2: WEB CODE & LIVE PLAYGROUND
# =========================================================
with tab2:
    st.markdown('<span class="vip-badge">LIVE PLAYGROUND</span>', unsafe_allow_html=True)
    st.markdown("### 💻 HTML/CSS Code Generator & Live Preview")
    voice_typing_widget("Web Requirement")
    
    web_req = st.text_input("🎯 Web Design Concept:", placeholder="e.g., Dark contact form with blue gradient button")
    
    if st.button("🚀 Generate Code & Render Preview", key="btn_web"):
        if web_req.strip() != "":
            html_code = f"""<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: sans-serif; background: #0f172a; color: white; padding: 25px; text-align: center; }}
    .card {{ background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.2); border-radius: 16px; padding: 20px; max-width: 380px; margin: 0 auto; }}
    input, button {{ width: 90%; padding: 10px; margin: 8px 0; border-radius: 8px; border: none; }}
    button {{ background: linear-gradient(90deg, #38bdf8, #818cf8); color: white; font-weight: bold; cursor: pointer; }}
</style>
</head>
<body>
    <div class="card">
        <h2>{web_req.title()}</h2>
        <input type="text" placeholder="Enter name...">
        <button>Submit</button>
    </div>
</body>
</html>"""
            col1, col2 = st.columns([1, 1])
            with col1:
                st.code(html_code, language="html")
            with col2:
                components.html(html_code, height=280, scrolling=True)

# =========================================================
# TAB 3: APP BUILDER
# =========================================================
with tab3:
    st.markdown('<span class="vip-badge">APP BUILDER</span>', unsafe_allow_html=True)
    st.markdown("### 📱 Mobile App Builder & Export Project (.ZIP)")
    voice_typing_widget("App Concept")
    
    app_name = st.text_input("🎯 App Name/Concept:", placeholder="e.g., Cloud Storage App 50GB")
    if st.button("🚀 Build App & Prepare ZIP", key="btn_app"):
        if app_name.strip() != "":
            flutter_code = f"// Flutter App Code: {app_name}\nimport 'package:flutter/material.dart';\nvoid main() => runApp(MaterialApp(home: Scaffold(body: Center(child: Text('{app_name}')))));"
            st.code(flutter_code, language="dart")
            zip_bytes = create_zip("main.dart", flutter_code)
            st.download_button(label="📦 Download Project (.ZIP)", data=zip_bytes, file_name=f"{app_name}.zip", mime="application/zip")

# =========================================================
# TAB 4: INSTANT PDF MAKER
# =========================================================
with tab4:
    st.markdown('<span class="vip-badge">PDF SUITE</span>', unsafe_allow_html=True)
    st.markdown("### 📄 Multilingual PDF Document Creator")
    voice_typing_widget("PDF Content")
    
    pdf_title = st.text_input("📌 PDF Heading:", placeholder="e.g., My AI Strategy File")
    pdf_body = st.text_area("📝 Content:", height=120)
    
    if st.button("🚀 Create PDF Document", key="btn_pdf"):
        if pdf_title.strip() != "" and pdf_body.strip() != "":
            pdf_bytes = create_pdf(pdf_title, pdf_body)
            st.download_button(label="📥 Download PDF File", data=bytes(pdf_bytes), file_name=f"{pdf_title}.pdf", mime="application/pdf")

# =========================================================
# TAB 5: AI ANIMATION SUITE
# =========================================================
with tab5:
    st.markdown('<span class="vip-badge">ANIMATION SUITE</span>', unsafe_allow_html=True)
    st.markdown("### 🎬 Sequential Animation Prompts")
    anim_req = st.text_input("🎯 Anime/Scene Story:", placeholder="e.g., Cyberpunk hero transformation")
    if st.button("🚀 Generate Prompts", key="btn_anim"):
        st.code(f"SCENE 1: Cinematic shot of {anim_req}, 8k anime style, 60fps.\nSCENE 2: Slow motion action.", language="text")

# =========================================================
# TAB 6: VIRALITY SCORE & SCRIPTS
# =========================================================
with tab6:
    st.markdown('<span class="vip-badge">VIRAL ANALYTICS</span>', unsafe_allow_html=True)
    st.markdown("### 📸 Virality Analyzer & Scripts")
    soc_topic = st.text_input("🎯 Video Topic:", placeholder="e.g., Top 5 AI tools")
    if st.button("🚀 Analyze & Generate Script", key="btn_soc"):
        st.metric("🔥 Viral Score", "95 / 100", "High Traffic")
        st.code(f"Hook: Don't miss this about {soc_topic}!\nCaption: Secret tools revealed! #{soc_topic.replace(' ','')}", language="text")

# =========================================================
# TAB 7: HD ICONS & STUDIO
# =========================================================
with tab7:
    st.markdown('<span class="vip-badge">IMAGE STUDIO</span>', unsafe_allow_html=True)
    st.markdown("### 🖼️ AI App Icon Studio")
    img_prompt = st.text_input("🎨 Image Prompt:", "Modern 3D app icon, isometric style, 4k quality")
    if st.button("✨ Generate Visual", key="btn_img"):
        encoded = urllib.parse.quote(img_prompt)
        st.image(f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true", use_column_width=True)

# =========================================================
# TAB 8: AI VOICE ENGINE
# =========================================================
with tab8:
    st.markdown('<span class="vip-badge">VOICE SUITE</span>', unsafe_allow_html=True)
    st.markdown("### 🎙️ Text-to-Speech Engine")
    voice_text = st.text_area("📝 Text to Voice:", "Welcome to StudioX Pro.", height=80)
    if st.button("🔊 Generate Voiceover", key="btn_voice"):
        tts = gTTS(text=voice_text, lang="en")
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format="audio/mp3")

# FOOTER
st.markdown("---")
components.html("<div style='text-align:center; color:#64748b; font-size:12px; font-weight:600;'>© 2026 StudioX Pro Ultra | Free Global Suite</div>", height=40)
