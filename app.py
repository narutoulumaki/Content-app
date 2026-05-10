import streamlit as st
import google.generativeai as genai
import json
from prompts import get_system_prompt, get_auto_suggest_prompt, HOOK_LIBRARY, FRAMEWORK_LIBRARY
from streamlit_mic_recorder import mic_recorder
from supabase import create_client

# 1. Page Config & Session State (The App's Memory)
st.set_page_config(page_title="CreatorBrain OS", layout="wide")

if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""
if "vibe" not in st.session_state:
    st.session_state.vibe = list(HOOK_LIBRARY.keys())[0]
if "framework" not in st.session_state:
    st.session_state.framework = list(FRAMEWORK_LIBRARY.keys())[0]

# 2. Supabase Connection
SUPABASE_URL = st.sidebar.text_input("Supabase URL", type="default")
SUPABASE_KEY = st.sidebar.text_input("Supabase Anon Key", type="password")

def save_to_db(dump, scripts, vibe, framework, niche):
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            data = {
                "user_dump": dump,
                "generated_scripts": scripts,
                "vibe": f"{vibe} | {framework}",
                "niche": niche
            }
            supabase.table("content_history").insert(data).execute()
            st.sidebar.success("Saved to History!")
        except Exception as e:
            st.sidebar.error(f"Database error: {e}")

# 3. Sidebar UI
with st.sidebar:
    st.header("⚙️ Strategy Settings")
    api_key = st.text_input("Gemini API Key", type="password")
    st.divider()
    
    # Dynamic Selectboxes that update based on AI suggestions
    vibe_idx = list(HOOK_LIBRARY.keys()).index(st.session_state.vibe) if st.session_state.vibe in HOOK_LIBRARY else 0
    st.session_state.vibe = st.selectbox("Strategy Vibe", list(HOOK_LIBRARY.keys()), index=vibe_idx)
    
    framework_idx = list(FRAMEWORK_LIBRARY.keys()).index(st.session_state.framework) if st.session_state.framework in FRAMEWORK_LIBRARY else 0
    st.session_state.framework = st.selectbox("Script Framework", list(FRAMEWORK_LIBRARY.keys()), index=framework_idx)
    
    niche = st.text_input("Creator Niche", "Hybrid Fitness")

# 4. Main App UI
st.title("🧠 CreatorBrain OS")
st.caption("Commute-to-Content: Step 1 (Dump & Analyze) -> Step 2 (Generate)")
st.divider()

# --- STEP 1: THE DUMP & TRANSCRIBE ---
st.subheader("Step 1: The Brain Dump")
col_audio, col_text = st.columns([1, 2])

with col_audio:
    st.write("🎤 Record Audio")
    audio = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop Recording", key='recorder')
    
    if audio and api_key:
        if st.button("Transcribe & Analyze 🗣️"):
            with st.spinner("Transcribing and analyzing strategy..."):
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Part A: Transcribe
                transcribe_prompt = "Transcribe the following audio exactly as spoken. Do not format it. Just raw text."
                resp_audio = model.generate_content([transcribe_prompt, {"mime_type": "audio/wav", "data": audio['bytes']}])
                st.session_state.raw_text = resp_audio.text
                
                # Part B: Auto-Suggest
                auto_prompt = get_auto_suggest_prompt(st.session_state.raw_text)
                resp_suggest = model.generate_content(auto_prompt)
                
                try:
                    # Clean markdown if Gemini wraps it in ```json
                    clean_json = resp_suggest.text.replace('```json', '').replace('```', '').strip()
                    suggestion = json.loads(clean_json)
                    st.session_state.vibe = suggestion.get("vibe", st.session_state.vibe)
                    st.session_state.framework = suggestion.get("framework", st.session_state.framework)
                    st.success("Strategy auto-selected in sidebar!")
                except:
                    st.warning("Transcription complete, but auto-suggest couldn't parse the JSON.")
                
                st.rerun()

with col_text:
    user_dump = st.text_area("📝 Edit Your Dump", value=st.session_state.raw_text, height=200)
    
    # Fallback button if user types text manually instead of recording
    if st.button("🪄 Auto-Suggest Strategy (For Typed Text)"):
        if user_dump and api_key:
            with st.spinner("Analyzing text..."):
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                auto_prompt = get_auto_suggest_prompt(user_dump)
                resp_suggest = model.generate_content(auto_prompt)
                try:
                    clean_json = resp_suggest.text.replace('```json', '').replace('```', '').strip()
                    suggestion = json.loads(clean_json)
                    st.session_state.vibe = suggestion.get("vibe", st.session_state.vibe)
                    st.session_state.framework = suggestion.get("framework", st.session_state.framework)
                    st.session_state.raw_text = user_dump # save their manual edits
                    st.rerun()
                except:
                    st.error("Failed to parse AI suggestion.")

st.divider()

# --- STEP 2: THE GENERATION ---
st.subheader("Step 2: Generate Short-Form Script")

if st.button("Generate & Save Scripts 🔥", use_container_width=True):
    if not api_key:
        st.error("Missing Gemini API Key!")
    elif not user_dump:
        st.warning("Please provide a text dump or transcribe some audio first!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            sys_prompt = get_system_prompt(st.session_state.vibe, st.session_state.framework, niche)
            
            with st.spinner(f"Applying '{st.session_state.vibe}' + '{st.session_state.framework}'..."):
                response = model.generate_content(f"{sys_prompt}\n\nUSER DUMP:\n{user_dump}")
                
                st.markdown("### 🎬 Your Short-Form Scripts")
                st.markdown(response.text)
                
                save_to_db(user_dump, response.text, st.session_state.vibe, st.session_state.framework, niche)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")