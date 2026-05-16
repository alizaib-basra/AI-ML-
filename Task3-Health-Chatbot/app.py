"""
app.py — HealthBot Flask Backend
AI/ML Internship Task 4: General Health Query Chatbot
"""

from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import requests
import os 

app = Flask(__name__)
app.secret_key = 'healthbot-secret-key-2024'

# ── Paste your FREE OpenRouter API key here ───────────────────────────────────

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# ── Call OpenRouter API ───────────────────────────────────────────────────────
def ask_model(prompt):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek/deepseek-v4-flash:free",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    data = response.json()
    return data['choices'][0]['message']['content']

# ── System Prompt (Prompt Engineering) ───────────────────────────────────────
SYSTEM_PROMPT = """
You are HealthBot, a friendly and knowledgeable general health assistant.

Your role:
- Answer general health questions in a warm, clear, and easy-to-understand way
- Use simple language that anyone can understand (avoid complex medical jargon)
- Keep responses concise but informative (3-5 sentences ideally)
- Always show empathy and care in your responses
- Format responses cleanly without using markdown asterisks or hashtags

Safety rules you MUST follow:
- NEVER provide specific medication dosages or prescriptions
- ALWAYS recommend consulting a real doctor for serious, severe, or persistent symptoms
- NEVER diagnose a specific disease or condition
- If a question sounds like a medical emergency, immediately tell the user to call emergency services
- Add a gentle reminder that you are an AI and not a substitute for professional medical advice

Tone: Friendly, caring, calm, and professional.
"""


# ── Safety Filter Keywords ────────────────────────────────────────────────────
EMERGENCY_KEYWORDS = [
    'chest pain', 'heart attack', "can't breathe", 'cannot breathe',
    'difficulty breathing', 'stroke', 'unconscious', 'not breathing',
    'severe bleeding', 'overdose', 'suicide', 'poisoning', 'seizure'
]

HARMFUL_KEYWORDS = [
    'how to overdose', 'lethal dose', 'kill myself',
    'how much to take to die', 'how to get high on'
]


def safety_filter(query):
    """Pre-checks query for emergencies or harmful intent."""
    query_lower = query.lower()

    for keyword in EMERGENCY_KEYWORDS:
        if keyword in query_lower:
            return False, (
                "🚨 This sounds like a medical emergency! "
                "Please call emergency services immediately: "
                "Pakistan: 115 or 1122 | Universal: 112. "
                "Do not wait — please seek help right now!"
            )

    for keyword in HARMFUL_KEYWORDS:
        if keyword in query_lower:
            return False, (
                "I'm sorry, but I can't help with that request. "
                "If you're going through a difficult time, please reach out "
                "to someone you trust or contact a mental health helpline."
            )

    return True, ""


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    """Serve the main chat page."""
    session['history'] = []
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend."""
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'response': 'Please type a message!', 'is_safe': True})

    # ── Safety Filter ─────────────────────────────────────────────────────────
    is_safe, safety_msg = safety_filter(user_message)
    if not is_safe:
        return jsonify({'response': safety_msg, 'is_safe': False, 'is_emergency': True})

    # ── Build conversation history ────────────────────────────────────────────
    history = session.get('history', [])
    history_text = ""
    for turn in history[-6:]:
        history_text += f"User: {turn['user']}\nHealthBot: {turn['bot']}\n\n"

    full_prompt = f"{SYSTEM_PROMPT}\n\n{history_text}User: {user_message}\nHealthBot:"

    # ── Call OpenRouter API ───────────────────────────────────────────────────
    try:
        bot_response = ask_model(full_prompt)
    except Exception as e:
        bot_response = f"Sorry, I encountered an error. Please try again. ({str(e)})"

    # ── Save to session history ───────────────────────────────────────────────
    history.append({'user': user_message, 'bot': bot_response})
    session['history'] = history

    return jsonify({'response': bot_response, 'is_safe': True})


@app.route('/reset', methods=['POST'])
def reset():
    """Clear the conversation history."""
    session['history'] = []
    return jsonify({'status': 'reset'})


if __name__ == '__main__':
    app.run(debug=True)