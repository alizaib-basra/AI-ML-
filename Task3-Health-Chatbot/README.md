# 🏥 General Health Query Chatbot
### AI/ML Internship – Task 4

---

## 🎯 Task Objective

Build a chatbot that answers general health-related questions using a Large Language Model (LLM). The chatbot uses **prompt engineering** to respond in a friendly, clear, and safe manner — while preventing harmful or dangerous medical advice.

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|---|---|
| **Google Gemini 1.5 Flash** | Free LLM API for generating responses |
| **Prompt Engineering** | Shape the AI's persona and safety behavior |
| **Keyword Safety Filter** | Pre-filter dangerous or emergency queries |
| **Python** | Core programming language |
| **Jupyter Notebook** | Development and demonstration environment |

---

## 🧠 Prompt Engineering Approach

The system prompt instructs the LLM to:
- Act as **HealthBot** — a friendly, knowledgeable health assistant
- Use **simple, jargon-free language** anyone can understand
- Always **recommend seeing a doctor** for serious symptoms
- Never provide **specific dosages or diagnoses**
- Show **empathy and care** in every response

---

## 🛡️ Safety System

A **two-layer safety system** protects users:

### Layer 1: Keyword Pre-Filter
- Detects **emergency keywords** (e.g., "chest pain", "heart attack") → redirects to emergency services immediately
- Detects **harmful queries** → refuses to answer with supportive message

### Layer 2: LLM-Level Safety (via Prompt)
- System prompt instructs the model to always add medical disclaimers
- Never diagnose or prescribe
- Always recommend professional consultation

---

## 📋 Example Queries & Responses

| Query | Behavior |
|---|---|
| "What causes a sore throat?" | Friendly, clear explanation with home remedy tips |
| "Is paracetamol safe for children?" | General safety info + recommend consulting a doctor |
| "I think I'm having a heart attack" | 🚨 Emergency redirect — call emergency services |
| "How much water should I drink?" | General health advice with friendly tone |

---

## 🚀 How to Run

### 1. Get Free API Key
- Go to [aistudio.google.com](https://aistudio.google.com)
- Sign in → Click **"Get API Key"** → **"Create API Key"**
- Copy your key

### 2. Install Dependencies
```bash
pip install google-generativeai
```

### 3. Open Notebook
```bash
jupyter notebook health_chatbot.ipynb
```

### 4. Add API Key
In **Section 2**, replace:
```python
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```
with your actual key.

### 5. Run All Cells
`Kernel → Restart & Run All` ✅

---

## 📁 Repository Structure

```
Task4-Health-Chatbot/
├── health_chatbot.ipynb    ← Main Jupyter Notebook
└── README.md               ← This file
```

---

## ⚠️ Disclaimer

> This chatbot is for **educational purposes only**. It provides general health information and is **NOT a substitute for professional medical advice**. Always consult a qualified healthcare professional for medical concerns.

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)
![Gemini](https://img.shields.io/badge/Google-Gemini_API-brightgreen?logo=google)

---

*Part of AI/ML Internship Task Series*
