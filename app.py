import streamlit as st
import base64
from scene_loader import get_themes, get_random_query
from retriever import hybrid_retrieval
from llm import generate_story

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Ramayana Story Explorer",
    layout="wide"
)

# ---------- HELPER ----------
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_img = get_base64_image("bg/ramayana_bg.png")

# ---------- RESPONSIVE CSS ----------
st.markdown(f"""
<style>

.stApp {{
    background-image: url("data:image/jpg;base64,{bg_img}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* overlay */
.stApp::before {{
content:"";
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:rgba(0,0,0,0.35);
z-index:-1;
}}

.title {{
font-size:46px !important;
text-align:center;
font-weight:bold;
color:white;
text-shadow:2px 2px 6px black;
margin-bottom: 10px;
}}

.control-box {{
background: rgba(255, 250, 240, 0.95);
padding:18px;
border-radius:12px;
border:2px solid #e0b96c;
margin-bottom:15px;
color: #2b2b2b;
box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}}

.story-box {{
background: rgba(60,50,22,0.9);
padding:25px;
border-radius:15px;
border:2px solid #e0b96c;
font-size:18px;
line-height:1.7;
color:white;
}}

.source-box {{
background: rgba(60,50,22,0.9);
border-left:6px solid #ff9933;
padding:10px;
margin-bottom:10px;
border-radius:6px;
color:white;
}}

div.stButton > button {{
background: linear-gradient(135deg,#ff9933,#ffcc66);
border-radius:10px;
border:none;
padding:10px;
font-weight:600;
width:100%;
}}

/* THEME CARD STYLE */
.theme-btn button {{
height:60px;
font-size:16px;
}}

/* -------- MOBILE -------- */
@media (max-width: 768px) {{

    .title {{
        font-size:28px !important;
    }}

    .story-box {{
        font-size:15px;
        padding:15px;
    }}

    .control-box {{
        padding:12px;
        font-size:14px;
    }}

    div.stButton > button {{
        font-size:16px;
        padding:12px;
    }}
}}

</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown('<p class="title">📜 Ramayana Story Explorer</p>', unsafe_allow_html=True)

themes = sorted(get_themes())

# ---------- RESPONSIVE DETECTION ----------
# fallback approach
is_mobile = st.session_state.get("is_mobile", False)

# ---------- LAYOUT ----------
if is_mobile:
    left_col = st.container()
    right_col = st.container()
else:
    left_col, right_col = st.columns([1.2, 2.8])

# ================= LEFT PANEL =================
with left_col:

    selected_theme = st.session_state.get("theme")

    generate_clicked = st.button("✨ Generate Story")

    if selected_theme:
        st.markdown(f"""
        <div class="control-box">
        <b>Selected Theme:</b><br>{selected_theme}
        </div>
        """, unsafe_allow_html=True)

    if generate_clicked:

        if not selected_theme:
            st.warning("⚠️ Select a theme first!")
        else:
            query = get_random_query(selected_theme)

            st.markdown(f"""
            <div class="control-box">
            <b>Scene Prompt:</b><br>{query}
            </div>
            """, unsafe_allow_html=True)

            with st.spinner("🔎 Retrieving Ramayana verses..."):
                contexts = hybrid_retrieval(query)

            with st.spinner("📖 Generating story..."):
                story = generate_story(query, contexts)

            st.session_state["story"] = story
            st.session_state["contexts"] = contexts
            st.session_state["scroll"] = True

            st.success("✅ Story generated! Scroll down 📖👇")

# ================= RIGHT PANEL =================
with right_col:

    st.subheader("Choose a Theme")

    # responsive grid
    num_cols = 4
    if is_mobile:
        num_cols = 2

    cols = st.columns(num_cols)

    for i, theme in enumerate(themes):
        col = cols[i % num_cols]

        with col:
            if st.button(theme, key=f"theme_{theme}"):
                st.session_state["theme"] = theme

# ---------- SCROLL ----------
st.markdown("<div id='story_section'></div>", unsafe_allow_html=True)

if st.session_state.get("scroll"):
    st.markdown(
        """
        <script>
        const section = window.parent.document.getElementById("story_section");
        if(section){
            section.scrollIntoView({behavior: "smooth"});
        }
        </script>
        """,
        unsafe_allow_html=True
    )
    st.session_state["scroll"] = False

# ================= STORY OUTPUT =================
if "story" in st.session_state:

    st.divider()

    st.subheader("📖 Generated Story")

    st.markdown(f"""
    <div class="story-box">
    {st.session_state["story"]}
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📚 Source Passages")

    for c in st.session_state["contexts"]:

        with st.expander(f"{c.metadata.get('kanda')} — {c.metadata.get('canto')}"):

            st.markdown(f"""
            <div class="source-box">
            {c.page_content[:500]}...
            </div>
            """, unsafe_allow_html=True)