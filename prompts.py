# prompts.py
import json

HOOK_LIBRARY = {
    "The Truth & Myths (Logic/Curiosity)": [
        "Most people dont have enough [X] but only because they dont understand this one thing",
        "This is exactly how much you have to [X] to get [Y]",
        "The brutal truth about [niche thing]",
        "The truth about [common belief] no one ever tells you.",
        "Here's why this never works the way people say it does.",
        "You don't need more [X], you need [Y].",
        "What [X] doesn't want you to know about.",
        "You've been lied to about this your whole life.",
        "Everything changes the moment you stop doing [X] and start [Y].",
        "The biggest lie you've been told about [X] is this.",
        "Everyone's lying about [X].",
        "I can't believe no one warned me about [X].",
        "The harsh truth: [X] is killing your chances of [Y].",
        "What no one tells you about [Problem]... and why it's keeping you stuck.",
        "I used to believe [Myth], until I realized [Truth].",
        "I think I just discovered the best [Process] ever.",
        "The moment I realized [Realization], everything changed.",
        "Nobody knows this but...",
        "One of the most underrated skills in life is...",
        "I wish I could transfer this understanding to everyone's brains",
        "Can you actually [Result] in [Time]?",
        "Is it possible for a complete beginner to [Result]?",
        "This is literally the easiest way to...",
        "But what they don't tell you is...",
        "The uncomfortable reason your [X] isn't [Y] actually.",
        "Everyone thinks [X] works... until they learn the brutal truth.",
        "[X] isn't [Y]... it is [Z].",
        "The real reason your [X] isn't [growing/improving].",
        "Are you tired of wasting money on [X]?",
        "Why haven't you found a solution to [Problem] yet?",
        "Don't assume [X] will fix your problems."
    ],
    "Aggressive Call-outs (Pattern Interrupt)": [
        "Stop doing [X] before it completely destroys your [Y]",
        "Avoid [X] if you want [Y].",
        "If you keep doing [X], you'll never achieve [Y].",
        "This is exactly what NOT to do.",
        "Stop doing this if you care about your [health/money/etc].",
        "Don't even try to [Goal] until you fix this first.",
        "This might hurt to hear, but it's true...",
        "If you keep doing [Action], you'll regret it later.",
        "I don't want to sound rude, but...",
        "The biggest mistake you're making in [X].",
        "This tiny mistake is silently ruining your [Result].",
        "If you ignore [X], don't be shocked when [Y] collapses.",
        "You're sabotaging your [Goal] every time you do [Action].",
        "Most people fail at [X] because they never fix [Y].",
        "Don't touch [X] until you hear this.",
        "I shouldn't reveal this but F*** it",
        "If your [X] looks like this and not like this...",
        "Let me de-influence you on...",
        "The worst advice I ever got about [Topic].",
        "Stereotypes I fell victim to after [Action].",
        "3 signs you're actually overtraining (Number 2 is scary).",
        "Don't even try to [Goal] until you fix this first."
    ],
    "Story & Relatability (Connection)": [
        "You won't believe what happens when you finally try [X].",
        "Realistic sacrifices you should make to [get Result].",
        "So I paid [Amount] to see [Person/Expert].",
        "I'm [Age] and embarrassed to admit...",
        "5 things no one told me about [Topic].",
        "I used to look like this... because of this [Photo/Action].",
        "Most men/women think they have good [Result] until they...",
        "Everything I would buy as a [Niche].",
        "I wish more men/women knew that...",
        "Pov you're a [Specific Niche] who wants to [Goal] and you find my page.",
        "I did [Hard Task] so you don't have to. Here's exactly what happened...",
        "I posted every day for 30 days so you don't have to. Here's exactly what happened...",
        "The biggest lesson I learnt about [X] and why it matters.",
        "This is something I learned way too late in my career.",
        "I thought I'd never overcome [Challenge], but here's what changed.",
        "The biggest mistake I made when I started [Journey].",
        "I remember feeling completely [Emotion] until I discovered [Solution].",
        "If you're [Specific Situation], this is for you. Here's how I overcame it.",
        "When [Challenge] happened, I had two choices. I chose [B].",
        "You look happier. Thanks I [Action].",
        "I wish more [X] did [Y].",
        "I wish more [X] knew that [Y].",
        "If you feel like you've been really consistent at [X] but not seeing results...",
        "I remember feeling completely [Emotion] until I discovered [Solution]."
    ],
    "The Matrix Logic (Psychological Triggers)": [
        "The Secret: What nobody tells you about [Hybrid Training]...",
        "The Timeline: How I went from [Problem] to [Result] in [X] weeks.",
        "The Contrast: You don't need [Expensive Tool]; you need [Basic Habit].",
        "The Authority: I've spent [X] years in the gym so you don't have to.",
        "The 'Why': The real reason your [Muscle Group] isn't growing.",
        "The Checklist: 3 signs you're actually overtraining (Number 2 is scary).",
        "The Call-out: If you're a [Niche/Target Audience], listen to this.",
        "The Myth: They lied to you about [Common Fitness Belief].",
        "The Relatability: POV: You finally figured out [Fitness Solution]."
    ]
}

FRAMEWORK_LIBRARY = {
    "PAS (Problem-Agitate-Solve)": "Start with the Hook. Agitate the pain point in 1 sentence. Provide the quick 1-step solution. End with a strong CTA.",
    "The Value Bomb": "Start with the Hook. Deliver 3 rapid-fire facts or steps. No fluffy transitions. Pure value. End with a CTA.",
    "The Contrarian": "Start with the Hook stating a common myth. Immediately state the exact opposite. Briefly explain why. End with a CTA.",
    "SB7 (StoryBrand)": "Start with the Hook. Identify Character desire -> State Problem -> Position as Guide -> Give 3-step Plan -> Success/Failure -> CTA."
}

def get_system_prompt(vibe, framework, niche="Hybrid Fitness"):
    selected_hooks = "\n".join(HOOK_LIBRARY.get(vibe, []))
    framework_rules = FRAMEWORK_LIBRARY.get(framework, "")
    
    return f"""
    ACT as a world-class Social Media Strategist and Ghostwriter for {niche} creators. 
    
    STRICT CONSTRAINTS (CRITICAL):
    1. SHORT-FORM ONLY: These scripts are for 30-60 second Instagram Reels. 
    2. WORD LIMIT: Max 100-120 words per script. Keep it highly punchy.
    3. NO YOUTUBE FLUFF: No "Welcome back guys" or "Let's dive in". Cut the fat.
    
    MARKETING PSYCHOLOGY RULES:
    1. THE JARGON TRANSLATOR: Never use clinical/scientific terms in the Hook (e.g., use "Shoulders" instead of "Rotator Cuff"). Save science for the body.
    2. THE BAIT & SWITCH: If using an aggressive "Stop doing [Exercise]" hook, you MUST add an "if condition" and clarify in the body that the exercise itself isn't bad.
    
    HOOK TEMPLATES TO USE (Pick 2):
    {selected_hooks}
    
    SCRIPT FRAMEWORK TO FOLLOW:
    {framework_rules}
    
    DIRECTIONS: 
    1. Analyze the User Dump.
    2. Select the 2 most impactful Hook Templates from the provided list. DO NOT write your own hooks.
    3. Fill the templates with specific words from the dump.
    4. Write the scripts following the exact SCRIPT FRAMEWORK provided above.
    
    TONE: High-energy, No-BS, authoritative.
    """

def get_auto_suggest_prompt(user_dump):
    return f"""
    Analyze the following raw text from a fitness creator. 
    Based on the tone and content, select the best matching 'Vibe' and 'Framework' from the lists below.
    
    Available Vibes: {list(HOOK_LIBRARY.keys())}
    Available Frameworks: {list(FRAMEWORK_LIBRARY.keys())}
    
    Return ONLY a raw JSON object (no markdown, no backticks). Format:
    {{"vibe": "Exact Vibe Name", "framework": "Exact Framework Name"}}
    
    TEXT:
    {user_dump}
    """