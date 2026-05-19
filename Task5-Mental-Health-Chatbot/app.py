"""
app.py — Mental Health Support Chatbot
AI/ML Internship Task 5
Streamlit Interface
"""

import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MindEase — Mental Health Chatbot",
    page_icon="🧠",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }

    /* Chat messages */
    .user-msg {
        background: #1e3a5f;
        border: 1px solid #2563eb;
        border-radius: 16px 16px 4px 16px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #e2e8f0;
        max-width: 80%;
        margin-left: auto;
    }
    .bot-msg {
        background: #1a1d27;
        border: 1px solid #2e3348;
        border-radius: 16px 16px 16px 4px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #e2e8f0;
        max-width: 80%;
    }
    .emotion-badge {
        background: #166534;
        color: #4ade80;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 12px;
        margin-bottom: 8px;
        display: inline-block;
    }
    .disclaimer {
        background: #2d1515;
        border: 1px solid #ef4444;
        border-radius: 10px;
        padding: 10px 14px;
        color: #fca5a5;
        font-size: 13px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Model ────────────────────────────────────────────────────────────────
MODEL_PATH = './mental-health-bot-final'
FALLBACK_MODEL = 'distilgpt2'

device = 'cuda' if torch.cuda.is_available() else 'cpu'

@st.cache_resource
def load_model():
    """Load the fine-tuned model or fallback to base model."""
    path = MODEL_PATH if os.path.exists(MODEL_PATH) else FALLBACK_MODEL
    label = 'fine-tuned' if os.path.exists(MODEL_PATH) else 'base (not fine-tuned)'
    tokenizer = AutoTokenizer.from_pretrained(path)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(path).to(device)
    return model, tokenizer, label

model, tokenizer, model_label = load_model()

# ── Response Generator ────────────────────────────────────────────────────────
def generate_response(user_input, emotion, max_new_tokens=80):
    """Generate an empathetic response."""
    prompt = f"Emotion: {emotion}\nUser: {user_input}\nBot:"
    inputs = tokenizer(
        prompt,
        return_tensors='pt',
        truncation=True,
        max_length=128
    ).to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.8,
            top_p=0.92,
            repetition_penalty=1.3,
            pad_token_id=tokenizer.eos_token_id
        )

    full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = full_text.split('Bot:')[-1].strip()

    # Clean up response
    if '\n' in response:
        response = response.split('\n')[0].strip()

    return response if response else "I'm here for you. Please tell me more about how you're feeling."


# ── UI ────────────────────────────────────────────────────────────────────────
st.title("🧠 MindEase")
st.caption("A safe space to express your feelings — powered by AI")
st.caption(f"Model: DistilGPT2 ({model_label})")

# Disclaimer
st.markdown("""
<div class="disclaimer">
⚠️ <strong>Important:</strong> MindEase is an AI chatbot for emotional support only.
It is NOT a substitute for professional mental health care.
If you are in crisis, please call <strong>115</strong> (Pakistan) or <strong>112</strong> (Universal).
</div>
""", unsafe_allow_html=True)

# Emotion selector
EMOTIONS = [
    "anxious", "sad", "lonely", "angry", "stressed",
    "hopeful", "grateful", "neutral", "joyful", "overwhelmed"
]

emotion = st.selectbox(
    "How are you feeling right now?",
    EMOTIONS,
    index=6
)

st.divider()

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        'role': 'bot',
        'content': "Hello! I'm MindEase 🧠 I'm here to listen and support you. How are you feeling today? Don't hesitate to share anything on your mind.",
        'emotion': None
    })

# Display chat history
for msg in st.session_state.messages:
    if msg['role'] == 'user':
        st.markdown(f"""
        <div class="user-msg">
            <span class="emotion-badge">😊 {msg.get('emotion', '')}</span><br>
            👤 {msg['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-msg">
            🧠 {msg['content']}
        </div>
        """, unsafe_allow_html=True)

# Input
st.divider()
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "Share your thoughts...",
        placeholder="Type how you're feeling...",
        label_visibility="collapsed"
    )
with col2:
    send = st.button("Send 💬", use_container_width=True)

# Clear button
if st.button("🔄 New Conversation", use_container_width=False):
    st.session_state.messages = [{
        'role': 'bot',
        'content': "Hello again! I'm here to listen. How are you feeling?",
        'emotion': None
    }]
    st.rerun()

# Handle message
if send and user_input.strip():
    # Add user message
    st.session_state.messages.append({
        'role': 'user',
        'content': user_input,
        'emotion': emotion
    })

    # Generate response
    with st.spinner('MindEase is thinking...'):
        response = generate_response(user_input, emotion)

    # Add bot response
    st.session_state.messages.append({
        'role': 'bot',
        'content': response,
        'emotion': None
    })

    st.rerun()
