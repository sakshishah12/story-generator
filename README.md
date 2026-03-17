# 📜 Ramayana Story Generator

An AI-powered storytelling platform that generates **context-aware, child-friendly stories from the Ramayana** using a hybrid retrieval system and large language models.

---

## 🌟 Overview

Ramayana Story Generator is an interactive web application that allows users to explore themes from the Ramayana and generate engaging stories grounded in original verses.

The system combines:

* 📚 Retrieval of relevant scripture passages
* 🧠 AI-based story generation
* 🎨 A visually immersive, Ramayana-inspired UI

---

## 🚀 Features

* 🎯 **Theme-based Story Generation**

  * Choose from **400+ curated themes** (e.g., courage, friendship, duty)

* 🔎 **Hybrid Retrieval System**

  * Combines:

    * FAISS (semantic similarity)
    * BM25 (keyword relevance)
  * Ensures contextually accurate verse retrieval

* 📖 **AI Story Generation**

  * Uses **Google Gemini (Flash)** to generate coherent, engaging narratives
  * Optimized for **child-friendly storytelling**

* 🖼️ **Interactive UI**

  * Custom Streamlit interface with:

    * Ramayana-themed background
    * Grid-based theme selection
    * Scroll-triggered story display
    * Expandable source passages

* 📚 **Source Transparency**

  * Displays original verses used to generate each story

---

## 🧠 System Architecture

```
User selects theme
        ↓
Random scene query generated
        ↓
Hybrid Retrieval (FAISS + BM25)
        ↓
Relevant Ramayana verses
        ↓
LLM (Gemini) generates story
        ↓
Story + source passages displayed
```

---

## 🛠️ Tech Stack

### 💻 Backend

* Python
* LangChain
* FAISS (Vector Search)
* BM25 (rank_bm25)

### 🤖 AI / ML

* Google Gemini API (gemini-flash-latest)
* HuggingFace Embeddings

### 🌐 Frontend

* Streamlit
* Custom CSS styling

### ☁️ Deployment

* Streamlit Cloud
* GitHub

---

## 📂 Project Structure

```
story_generator/
│
├── app.py                # Streamlit UI
├── llm.py                # Gemini integration
├── retriever.py         # Hybrid retrieval logic
├── scene_loader.py      # Themes + queries
├── data/                # Ramayana dataset
├── bg/                  # UI background image
├── requirements.txt
└── README.md
```

---

## 🔧 Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/sakshishah12/story-generator.git
cd story-generator
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Add API Key

#### 🔐 For Local Development

Create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
```

---

#### ☁️ For Streamlit Deployment

Go to:

```
App Settings → Secrets
```

Add:

```toml
GOOGLE_API_KEY = "your_api_key_here"
```

---

### 4️⃣ Run App

```bash
streamlit run app.py
```

---

## ⚠️ Deployment Notes

* `.env` should **NOT be pushed to GitHub**
* Use `st.secrets` for production
* Add all dependencies in `requirements.txt`:

  * `rank_bm25`
  * `faiss-cpu`
  * `langchain`
  * `google-generativeai`

---

## 📊 Optimization Techniques

* 🔁 **Batch processing** to reduce API calls
* ⚡ **Hybrid retrieval** for accuracy + speed
* 🧠 **Prompt engineering** for structured storytelling
* 🧹 Cleaned dataset for **child-safe themes**

---

## 🎯 Use Cases

* 📚 Educational storytelling platform
* 🧒 Interactive learning for children
* 🧠 NLP + Retrieval system demonstration
* 📊 AI/ML portfolio project

---

## 🚧 Future Improvements

* 🔊 Voice narration (TTS)
* 🌍 Multilingual story generation
* 🧠 Fine-tuned LLM for mythological storytelling
* 📈 User analytics & personalization
* 💾 Story caching to reduce API usage

---

## 👩‍💻 Author

**Sakshi Shah**
MS in Data Science — Stony Brook University

* 💼 Interested in: ML, NLP, AI Systems
* 🔗 GitHub: https://github.com/sakshishah12

---

## ⭐ Key Highlights (for Recruiters)

* Built a **hybrid retrieval + LLM pipeline**
* Designed a **production-ready Streamlit application**
* Handled **API limits, deployment, and UI optimization**
* Focused on **real-world usability and storytelling experience**

---

## 📜 License

This project is for educational and research purposes.
