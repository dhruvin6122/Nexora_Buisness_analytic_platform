import streamlit as st
import time
import requests
import re
from streamlit_lottie import st_lottie

# API Configuration
API_URL = "http://localhost:8000"

class UserObj:
    """Helper to maintain object-like access for User data"""
    def __init__(self, data):
        self.id = data['id']
        self.full_name = data['full_name']
        self.email = data['email']

# --- 1. SETUP & CONFIG ---

# --- 1. SETUP & CONFIG ---
st.set_page_config(
    page_title="Nexora | Sales Analytics AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ASSETS & CACHING ---
# Auth wrapper removed

@st.cache_data(ttl=3600)
def load_lottie(url):
    try:
        r = requests.get(url, timeout=2)
        if r.status_code != 200: return None
        return r.json()
    except:
        return None

# Animations loaded lazily in login_ui

# --- 3. THEME & STYLING ---
st.markdown("""
<style>
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stStatusWidget"] {visibility: hidden;}
    [data-testid="stHeaderActionElements"] {visibility: hidden;}
    
    /* Ensure Sidebar Toggle is visible and clickable */
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible !important;
        display: block !important;
        z-index: 999999 !important;
        color: #60A5FA !important; /* Keep the theme blue */
    }
    
    /* Reduce top spacing */
    .block-container {
        padding-top: 1rem !important; /* Revert to standard override */
        padding-bottom: 0rem !important;
    }
    
    /* Chat Message Bubbles */
    .stChatMessage {
        padding: 1.5rem !important;
        margin-bottom: 1rem !important;
        border-radius: 16px !important;
        max-width: 85% !important;
        background-color: rgba(30, 41, 59, 0.5) !important; /* Dark bubble for AI */
        border: 1px solid rgba(71, 85, 105, 0.4) !important;
        font-size: 1.1rem !important;
        line-height: 1.6 !important;
    }
    
    /* User Message Specifics (Right Aligned, Blue) */
    .stChatMessage:has(.is-user) {
        max-width: 70% !important;
        margin-left: auto !important;
        background-color: rgba(59, 130, 246, 0.15) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Input Box Styling - Full Width */
    [data-testid="stChatInput"] {
        max-width: 100% !important;
        margin: 0 auto !important;
    }

    /* --- MOBILE OPTIMIZATION --- */
    @media only screen and (max-width: 768px) {
        /* Wider bubbles on phone */
        .stChatMessage {
            max-width: 95% !important;
            padding: 1rem !important;
        }
        
        /* User bubbles wider too, keep right align */
        .stChatMessage:has(.is-user) {
            max-width: 90% !important;
        }

        /* Lock Input to Bottom safely */
        [data-testid="stChatInput"] {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            z-index: 999;
        }
        
        /* Reduce side padding */
        .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- 3. THEME ---
# Using native Streamlit theme

# --- 4. STATE ---
if 'user' not in st.session_state: st.session_state.user = None
if 'messages' not in st.session_state: st.session_state.messages = []
if 'auth_state' not in st.session_state: st.session_state.auth_state = 'idle'
if 'auth_creds' not in st.session_state: st.session_state.auth_creds = {}
if 'auth_error' not in st.session_state: st.session_state.auth_error = None
if 'suggestions_clicked' not in st.session_state: st.session_state.suggestions_clicked = None

# --- 5. UI COMPONENTS ---

def login_ui():
    """Optimized Split-Screen Login to preserve requested theme flow"""
    
    # Load Assets Lazy (Only runs when User is NOT logged in)
    lottie_computer = load_lottie("https://lottie.host/5a83707e-7c3e-4613-8994-188b02220d9e/A06d3lW7hM.json")
    if not lottie_computer:
        lottie_computer = load_lottie("https://assets5.lottiefiles.com/packages/lf20_w51pcehl.json")
    lottie_loading = load_lottie("https://lottie.host/9320e8b2-385a-463e-9562-q965e60803c/p1.json")

    # Hide Sidebar on Login
    st.markdown("""<style>[data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)
    
    # Anchor for scrolling
    st.markdown("<div id='login-top'></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.1, 1], gap="large")
    
    with col1:
        st.markdown("<br><br><br><br>", unsafe_allow_html=True) # Push graphic down
        if lottie_computer:
            st_lottie(lottie_computer, height=500, key="computer_anim")
        else:
            st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71", caption="Nexora Analytics")

    with col2:
        # Persistent Header
        st.markdown("""
            <h1 style='text-align: center; color: #60A5FA; font-weight: 800; letter-spacing: -1px;
            text-shadow: 0 0 5px rgba(37, 99, 235, 0.3);'>Nexora</h1>
        """, unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #F8FAFC; margin-bottom: 2.5rem; font-size: 1.1rem;'>Sales Analytics AI Agent</p>", unsafe_allow_html=True)

        right_panel = st.empty()
        
        # Determine content based on state
        if st.session_state.auth_state == 'processing_login':
             # Force Scroll to Top - Persistent
             st.markdown("""
                <script>
                    function forceScroll() {
                        var footer = window.parent.document.querySelector('footer');
                        if (footer) { footer.style.display = 'none'; }
                        window.parent.window.scrollTo(0,0);
                    }
                    setTimeout(forceScroll, 10);
                    setTimeout(forceScroll, 100);
                    setTimeout(forceScroll, 500);
                </script>
             """, unsafe_allow_html=True)
             
             with right_panel.container():
                if lottie_loading:
                    st_lottie(lottie_loading, height=220, key="loading_login")
                else:
                    st.spinner("Processing...")
                st.markdown("<h3 style='text-align: center; color: #2563EB;'>Authenticating session...</h3>", unsafe_allow_html=True)
                
                creds = st.session_state.auth_creds
                try:
                    resp = requests.post(f"{API_URL}/auth/login", json={
                        "email": creds.get('email'), 
                        "password": creds.get('pwd')
                    })
                    if resp.status_code == 200:
                        u = UserObj(resp.json())
                        err = None
                    else:
                        u = None
                        err = resp.json().get('detail', 'Login failed')
                except Exception as e:
                    u = None
                    err = f"API Error: {e}"
                
                if u:
                    # Clear form
                    right_panel.empty()
                    
                    with right_panel:
                         with st.spinner("Loading Dashboard..."):
                                # 1. PREFETCH DATA (Ready Chatbot)
                                try:
                                    h_resp = requests.get(f"{API_URL}/auth/history/{u.id}", timeout=3)
                                    if h_resp.status_code == 200:
                                        st.session_state.messages = []
                                        for h in h_resp.json():
                                            st.session_state.messages.append({
                                                "role": h['role'],
                                                "content": h['content']
                                            })
                                except: pass
                                time.sleep(1.0) # Ensure sync visual

                    # 2. PREVENT OVERLAP (Kill Graphic)
                    col1.empty()

                    # 3. SWITCH
                    st.session_state.user = u
                    st.session_state.auth_state = 'idle'
                    st.rerun()
                else:
                    st.session_state.auth_state = 'idle'
                    st.session_state.auth_error = err
                    time.sleep(1)
                    st.rerun()

        elif st.session_state.auth_state == 'processing_signup':
            # Force Scroll to Anchor
            st.markdown("""
                <script>
                    function scrollToTop() {
                        var topDiv = window.parent.document.getElementById('login-top');
                        if (topDiv) {
                            topDiv.scrollIntoView({behavior: 'instant', block: 'start'});
                        } else {
                            // Fallback to window scroll
                            window.parent.window.scrollTo(0,0);
                        }
                    }
                    setTimeout(scrollToTop, 50);
                    setTimeout(scrollToTop, 200);
                    setTimeout(scrollToTop, 500);
                    setTimeout(scrollToTop, 1000); // Late check
                </script>
            """, unsafe_allow_html=True)

            with right_panel.container():
                if lottie_loading:
                    st_lottie(lottie_loading, height=220, key="loading_signup")
                else:
                    st.spinner("Creating account...")
                st.markdown("<h3 style='text-align: center; color: #2563EB;'>Setting up workspace...</h3>", unsafe_allow_html=True)
                
                creds = st.session_state.auth_creds
                try:
                    resp = requests.post(f"{API_URL}/auth/signup", json={
                        "full_name": creds.get('name'),
                        "email": creds.get('email'),
                        "password": creds.get('pwd')
                    })
                    if resp.status_code == 200:
                        u = UserObj(resp.json())
                        err = None
                    else:
                        u = None
                        err = resp.json().get('detail', 'Signup failed')
                except Exception as e:
                    u = None
                    err = f"API connection failed: {e}"
                
                if u:
                     st.balloons()
                     st.session_state.auth_state = 'idle'
                     st.success("Account created successfully! Please log in.")
                     # Remain on Sign Up tab
                     time.sleep(1.5)
                     st.rerun()
                else:
                     st.session_state.auth_state = 'idle'
                     st.session_state.auth_error = err
                     time.sleep(1)
                     st.rerun()
        
        else: # IDLE STATE - Render Forms
             with right_panel.container():
                if st.session_state.auth_error:
                    st.error(st.session_state.auth_error)
                    st.session_state.auth_error = None
                
                # Ensure radio key exists to avoid errors on First Run
                if 'auth_mode_select' not in st.session_state:
                    st.session_state.auth_mode_select = "Log In"

                st.subheader("Welcome")
                
                # Use Radio for programmable tab switching
                auth_mode = st.radio(
                    "Auth Navigation",
                    ["Log In", "Sign Up"],
                    horizontal=True,
                    label_visibility="collapsed",
                    key="auth_mode_select"
                )
                
                if auth_mode == "Log In":
                    st.write("") 
                    with st.form("login"):
                        email = st.text_input("User Email")
                        pwd = st.text_input("Password", type="password")
                        if st.form_submit_button("Log In", use_container_width=True):
                            st.session_state.auth_creds = {'email': email, 'pwd': pwd}
                            st.session_state.auth_state = 'processing_login'
                            st.rerun()
    
                elif auth_mode == "Sign Up":
                    st.write("") 
                    with st.form("signup"):
                        new_name = st.text_input("Full Name")
                        new_email = st.text_input("Email Address")
                        new_pwd = st.text_input("Create Password", type="password")
                        confirm_pwd = st.text_input("Confirm Password", type="password")
                        
                        if st.form_submit_button("Create Account", use_container_width=True):
                            # 1. Check Passwords Match
                            if new_pwd != confirm_pwd:
                                st.error("Passwords do not match!")
                            
                            # 2. Validate Email
                            elif not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
                                st.error("Please enter a valid email address.")

                            # 3. Validate Password Length
                            elif len(new_pwd) < 8:
                                st.error("Password must be at least 8 characters long.")

                            # 4. Validate Alphanumeric
                            elif not (re.search(r"[A-Za-z]", new_pwd) and re.search(r"[0-9]", new_pwd)):
                                st.error("Password must contain both letters and numbers.")
                                
                            else:
                                st.session_state.auth_creds = {'email': new_email, 'pwd': new_pwd, 'name': new_name}
                                st.session_state.auth_state = 'processing_signup'
                                st.rerun()

def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.015)

def chat_ui():
    """Clean Native Streamlit Chat UI"""

    # ---------- SIDEBAR ----------
    # ---------- SIDEBAR ----------
    with st.sidebar:
        # 1. Welcome User (Top)
        st.markdown(f"""
            <div style='text-align: center; margin-bottom: 1.5rem;'>
                <p style='color: #94A3B8; font-size: 0.9rem; margin-bottom: 0.2rem;'>Welcome back,</p>
                <h3 style='color: #F8FAFC; margin: 0; font-weight: 600;'>{st.session_state.user.full_name.split(' ')[0]}</h3>
            </div>
        """, unsafe_allow_html=True)

        # 2. Nexora AI (Centered below welcome)
        st.markdown("""
            <div style='text-align: center; margin-bottom: 1.5rem; background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 12px; border: 1px solid rgba(59, 130, 246, 0.2);'>
                <h2 style='color: #60A5FA; margin: 0; font-weight: 800; letter-spacing: -0.5px;'>Nexora AI</h2>
                <p style='color: #E2E8F0; font-size: 0.85rem; margin-top: 0.5rem;'>Your Intelligent Sales Analyst</p>
            </div>
        """, unsafe_allow_html=True)

        # 3. Short Features (Below Nexora AI)
        st.caption("CAPABILITIES")
        st.markdown("""
            <div style='display: flex; flex-direction: column; gap: 0.8rem; margin-bottom: 2rem;'>
                <div style='display: flex; align-items: center; gap: 0.8rem; color: #CBD5E1;'>
                    <span style='background: #1E293B; padding: 6px; border-radius: 6px;'>🔥</span>
                    <span style='font-size: 0.9rem;'>Find Top Selling Products</span>
                </div>
                <div style='display: flex; align-items: center; gap: 0.8rem; color: #CBD5E1;'>
                    <span style='background: #1E293B; padding: 6px; border-radius: 6px;'>📦</span>
                    <span style='font-size: 0.9rem;'>Track Inventory Levels</span>
                </div>
                <div style='display: flex; align-items: center; gap: 0.8rem; color: #CBD5E1;'>
                    <span style='background: #1E293B; padding: 6px; border-radius: 6px;'>📈</span>
                    <span style='font-size: 0.9rem;'>Analyze Customer Orders</span>
                </div>
                <div style='display: flex; align-items: center; gap: 0.8rem; color: #CBD5E1;'>
                    <span style='background: #1E293B; padding: 6px; border-radius: 6px;'>⚠️</span>
                    <span style='font-size: 0.9rem;'>Detect Low Stock Alerts</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Spacer
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # 4. Questions (Below Features)
        st.caption("TRY ASKING")
        demo_q = st.radio(
            "Select a question:",
            [
                "None", 
                "Show best selling products",
                "Which items are low on stock?",
                "Total revenue today",
                "List recent orders",
                "Count of pending orders",
                "Top 5 customers by spend",
                "Current inventory value",
                "Sales trends this week"
            ],
            index=0,
            label_visibility="collapsed",
            key="sidebar_q"
        )

        if demo_q and demo_q != "None":
            if st.button("🚀 Ask Question", use_container_width=True):
                 st.session_state.suggestions_clicked = demo_q
                 st.rerun()

        st.divider()

        # 5. Logout (Last)
        if st.button("🚪 Sign Out", use_container_width=True, type="primary"):
            st.session_state.user = None
            st.session_state.messages = []
            st.session_state.auth_state = "idle"
            st.rerun()

    # ---------- MAIN ----------
    # ---------- MAIN ----------
    st.markdown("""
        <div style='text-align: center; width: 100%; margin-top: 3rem; margin-bottom: 1.5rem;'>
            <h2 style='font-weight: 700; color: #F8FAFC; display: inline-block; font-size: 2.5rem; margin: 0;'>
                Sales Analytics Assistant
            </h2>
        </div>
    """, unsafe_allow_html=True)

    # Load chat history once
    if not st.session_state.messages:
        try:
            resp = requests.get(f"{API_URL}/auth/history/{st.session_state.user.id}")
            if resp.status_code == 200:
                history = resp.json()
                for h in history:
                    st.session_state.messages.append({
                        "role": h['role'],
                        "content": h['content']
                    })
        except:
            pass



    # ---------- SHOW MESSAGES ----------
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "✨"
        with st.chat_message(msg["role"], avatar=avatar):
            if msg["role"] == "user":
                # Inject marker for CSS targeting (Use span to avoid block-level breaks)
                st.markdown(f"<span style='display:none;' class='is-user'></span>{msg['content']}", unsafe_allow_html=True)
            else:
                st.markdown(msg["content"])

    # Logic for Sidebar Suggestions
    if 'suggestions_clicked' not in st.session_state:
        st.session_state.suggestions_clicked = None

    if st.session_state.suggestions_clicked:
         sidebar_prompt = st.session_state.suggestions_clicked
         st.session_state.suggestions_clicked = None
    else:
         sidebar_prompt = None

    # ---------- INPUT ----------
    user_input = st.chat_input("Ask about your business data...")
    
    # Use either the sidebar prompt or the user input
    prompt = sidebar_prompt if sidebar_prompt else user_input

    if prompt:
        # User message (Dedup Check)
        if not st.session_state.messages or st.session_state.messages[-1]["content"] != prompt:
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })

        with st.chat_message("user", avatar="👤"):
            st.markdown(f"<span style='display:none;' class='is-user'></span>{prompt}", unsafe_allow_html=True)

        # AI response
        with st.chat_message("assistant", avatar="✨"):
            full_response = ""
            
            # 1. Show Spinner while waiting for API
            with st.spinner("Nexora is analyzing your data..."):
                # Save User Message (Hidden latency)
                try:
                     requests.post(f"{API_URL}/auth/message", json={
                        "user_id": str(st.session_state.user.id),
                        "role": "user",
                        "content": prompt
                     })
                except: pass

                try:
                    # Message context
                    ctx = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages[-5:]
                    ]

                    # Call Agent API
                    payload = {
                        "input": prompt,
                        "user_id": str(st.session_state.user.id),
                        "history": ctx
                    }
                    api_resp = requests.post(f"{API_URL}/agent/chat", json=payload)
                    
                    if api_resp.status_code == 200:
                        full_response = api_resp.json()["output"]
                    else:
                        full_response = "I'm having trouble connecting to the server."

                except Exception as e:
                    full_response = f"Error: {e}"

            # 2. Spinner is gone. Now Stream the text.
            st.write_stream(stream_text(full_response))
            
            # 3. Append to State (So it stays on rerun)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # 4. Save to API
            try:
                requests.post(f"{API_URL}/auth/message", json={
                    "user_id": str(st.session_state.user.id),
                    "role": "assistant",
                    "content": full_response
                })
            except: pass

            # Chat loop end

# --- 6. ROOT ROUTER ---
if not st.session_state.user:
    login_ui()
else:
    chat_ui()
