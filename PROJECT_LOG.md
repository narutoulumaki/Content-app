📂 PROJECT LOG: CreatorBrain OS (As of MVP Phase 1)
1. Core Concept & Product Strategy

The Problem: Creators have great ideas on the go (like the bus) but lose the context before they can script them.

The Solution: "Commute-to-Content" micro-SaaS. Turns raw voice/text dumps into ready-to-film short-form scripts using custom hook templates and the StoryBrand 7 (SB7) framework.

Target Audience Pivot: Exclusively targeting short-form content (Reels/Shorts, ~30-60 seconds, max 120 words). Ignoring long-form (YouTube) for now to own a specific niche.

2. Architecture & Tech Stack

Current MVP Stack: Python, Streamlit (Frontend/Routing).

AI Engine: Gemini 2.5 Flash API (handling both text and direct .wav audio processing natively via multimodal capabilities).

Database: Supabase (PostgreSQL) for saving user dumps and generated scripts.

Future Production Stack: Ruby on Rails + Stimulus (Hotwire) + PostgreSQL. (Chosen for solo-founder speed and built-in auth/database routing).

3. UI/UX Decisions

Version 1 (Completed): Sidebar for API/DB config. Main split-screen with text dump on the left and streamlit-mic-recorder on the right. One-click "Generate & Save" button.

Version 2 (Next Up): The "Two-Step Human-in-the-Loop" UI.

Step 1: Audio recording transcribes to a text box (editable).

Step 2: AI auto-suggests a "Strategy Vibe" based on the text.

Step 3: User confirms vibe and generates the final script.

4. Prompt Engineering & Logic (prompts.py)

Implemented the SB7 Framework (Character, Problem, Guide, Plan, Call to Action).

Added Marketing Psychology Rules:

The Jargon Translator: Force the AI to use simple terms in the hook (e.g., "Shoulders" instead of "Rotator Cuff") to stop the scroll, saving science for the body.

The Bait & Switch: If using an aggressive "Stop doing this" hook, the AI must include an "if condition" and clarify the exercise isn't inherently bad.

### Milestone Update: UX Overhaul & Framework Diversity

**1. Content Strategy Pivot:**
* Realized the SB7 framework was forcing scripts to be too long for Instagram Reels/Shorts.
* Introduced a `FRAMEWORK_LIBRARY` decoupling "Vibe" (Hooks) from "Framework" (Structure).
* Added fast-paced frameworks: `PAS (Problem-Agitate-Solve)`, `The Value Bomb`, and `The Contrarian`.
* Enforced strict 100-120 word limits in `prompts.py`.

**2. UI/UX Refinement ("Human-in-the-Loop" Auto-Suggest):**
* Removed "invisible" state changes. The AI now transcribes the audio, analyzes the text, but **holds** the suggestion.
* Added a UI block below the text editor that displays: `💡 AI Suggests: [Vibe] + [Framework]`.
* Added an `✅ Apply This Strategy` button so the user retains complete control over their active sidebar settings.
* Ensured manual text edits in the `st.text_area` are preserved in session state when applying AI suggestions.