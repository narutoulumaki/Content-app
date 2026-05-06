import streamlit as st
import google.generativeai as genai
from prompts import get_system_prompt, HOOK_LIBRARY
from streamlit_mic_recorder import mic_recorder
from supabase import create_client

# 1. Page Config
st.set_page_config(page_title="CreatorBrain OS", layout="wide")

# 2. Supabase Connection
SUPABASE_URL = st.sidebar.text_input("Supabase URL", type="default")
SUPABASE_KEY = st.sidebar.text_input("Supabase Anon Key", type="password")

def save_to_db(dump, scripts, vibe, niche):
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            data = {
                "user_dump": dump,
                "generated_scripts": scripts,
                "vibe": vibe,
                "niche": niche
            }
            supabase.table("content_history").insert(data).execute()
            st.sidebar.success("Saved to History!")
        except Exception as e:
            st.sidebar.error(f"Database error: {e}")

# 3. Sidebar UI
with st.sidebar:
    st.header("⚙️ API Settings")
    api_key = st.text_input("Gemini API Key", type="password")
    st.divider()
    vibe = st.selectbox("Strategy Vibe", list(HOOK_LIBRARY.keys()))
    niche = st.text_input("Creator Niche", "Hybrid Fitness")

# 4. Main App UI
st.title("🧠 CreatorBrain OS")
st.caption("Commute-to-Content: Messy thoughts into viral scripts.")

col1, col2 = st.columns([2, 1])

with col1:
    user_dump = st.text_area("📥 The Brain Dump", height=300, placeholder="Paste notes here...")

with col2:
    st.write("🎤 Record Thought (Bus/Train Mode)")
    audio = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop Recording", key='recorder')
    if audio:
        st.audio(audio['bytes'])
        st.success("Audio captured! Ready for Gemini.")

# 5. Execution (The Multimodal Engine)
if st.button("Generate Scripts 🔥", use_container_width=True):
    if not api_key:
        st.error("Missing Gemini API Key! Add it in the sidebar.")
    elif not user_dump and not audio:
        st.warning("Please provide either a text dump or record an audio note!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            sys_prompt = get_system_prompt(vibe, niche)
            
            # Constructing the payload based on what the user provided
            prompt_parts = [sys_prompt]
            
            if user_dump:
                prompt_parts.append(f"\n\nUSER TEXT DUMP:\n{user_dump}")
                
            if audio:
                prompt_parts.append("\n\nUSER AUDIO DUMP: Listen to the attached audio recording to extract the content for the script.")
                # Pass the raw audio bytes directly to Gemini
                prompt_parts.append({"mime_type": "audio/wav", "data": audio['bytes']})
            
            with st.spinner("Analyzing your dump and writing scripts..."):
                response = model.generate_content(prompt_parts)
                
                # Display results
                st.divider()
                st.markdown("### 🎬 Your Scripts")
                st.markdown(response.text)
                
                # Save to Database (Note: We save a placeholder for audio if there's no text)
                db_dump_text = user_dump if user_dump else "[Audio Recording Processed]"
                save_to_db(db_dump_text, response.text, vibe, niche)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

# 6. History View
if st.checkbox("View Past History"):
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            history = supabase.table("content_history").select("*").order("created_at", desc=True).execute()
            for item in history.data:
                with st.expander(f"Dump from {item['created_at'][:10]} - {item['vibe']}"):
                    st.write("**Dump:**", item['user_dump'])
                    st.markdown(item['generated_scripts'])
        except Exception as e:
            st.error(f"Could not load history: {e}")