import google.generativeai as genai

# Paste your API key here inside the quotes
GOOGLE_API_KEY = "AIzaSyCw6wYonI3wYJp99Fl5EKXb9yg766IdHMA"

genai.configure(api_key=GOOGLE_API_KEY)

print("🔍 Checking your API Key for available models...")
print("-" * 40)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)