# 🧠 Mental Health Support Chatbot (Fine-Tuned)
### AI/ML Internship – Task 5

---

## 🎯 Task Objective

Build a chatbot that provides **empathetic and supportive** responses for stress, anxiety, and emotional wellness by fine-tuning a small LLM on real human empathetic conversations.

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|---|---|
| **DistilGPT2** | Base model for fine-tuning (82M parameters) |
| **EmpatheticDialogues** | Facebook AI dataset — 25,000 empathetic conversations |
| **Hugging Face Transformers** | Model loading, Trainer API, tokenization |
| **Hugging Face Datasets** | Loading EmpatheticDialogues |
| **Streamlit** | Web interface for the chatbot |
| **Google Colab** | Free GPU for training |

---

## 📚 Dataset

**EmpatheticDialogues** (Facebook AI Research):
- 25,000 conversations across 32 emotion categories
- Real human empathetic responses
- Emotions: anxious, sad, lonely, angry, joyful, grateful, etc.

---

## 🏋️ Fine-Tuning Process

```
Base DistilGPT2 Model
        ↓
Load EmpatheticDialogues dataset
        ↓
Format: "Emotion: {emotion}\nUser: {prompt}\nBot: {response}"
        ↓
Tokenize with max_length=128
        ↓
Train with Hugging Face Trainer API (3 epochs)
        ↓
Fine-Tuned Mental Health Chatbot ✅
```

---

## 🚀 How to Run

### Step 1: Fine-tune on Google Colab
1. Upload `train.ipynb` to [colab.research.google.com](https://colab.research.google.com)
2. Enable GPU: **Runtime → Change runtime type → T4 GPU**
3. Run all cells
4. Download `mental-health-bot-final.zip`
5. Extract into `Task5-Mental-Health-Chatbot/` folder

### Step 2: Run Streamlit App
```bash
cd Task5-Mental-Health-Chatbot
pip install -r requirements.txt
streamlit run app.py
```

### Step 3: Open browser
```
http://localhost:8501
```

> **Note:** If fine-tuned model is not found, the app falls back to base DistilGPT2 automatically.

---

## ⚠️ Disclaimer

> This chatbot is for **educational purposes only**. It is NOT a substitute for professional mental health care. If you are in crisis, please call **115** (Pakistan) or **112** (Universal Emergency).

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow?logo=huggingface)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?logo=streamlit)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep_Learning-orange?logo=pytorch)

---

*Part of AI/ML Internship Task Series*
