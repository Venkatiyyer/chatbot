
# 🚀 VenkyAI Assistant

VenkyAI is a GPT-like AI assistant built with a **FastAPI backend** and a **Streamlit frontend**. It supports intelligent chat using **Groq**, **LangChain**, and **Google Generative AI**, and is designed for easy cloud deployment on **Render** (backend) and **Streamlit Community Cloud** (frontend).

---

## ✨ Features

- 🤖 AI-powered chat assistant  
- ⚡ FastAPI backend with `/chat` endpoint  
- 🎨 Streamlit-based interactive UI  
- 🔐 Secure secrets management using `secrets.toml` and Streamlit Cloud  
- 🌐 Deployed on Render (Backend) + Streamlit Cloud (Frontend)  
- 📄 PDF support using PyPDF2  
- 🔗 RAG-ready stack with LangChain  

---

## 🛠 Tech Stack

### Backend
- FastAPI  
- Uvicorn  
- Groq  
- LangChain  
- LangChain-Groq  
- LangChain-Google-GenAI  
- Python-Dotenv  

### Frontend
- Streamlit  
- Requests  

### AI & Utilities
- PyPDF2  

---

## 📁 Project Structure

```

📦 venkyai/
┣ 📂 backend/
┃ ┣ 📄 backend.py
┃ ┣ 📄 requirements.txt
┃ ┗ 📄 runtime.txt
┣ 📂 frontend/
┃ ┣ 📄 app.py
┃ ┗ 📂 .streamlit/
┃   ┗ 📄 secrets.toml  (local only)
┣ 📄 README.md
┗ 📄 .gitignore

```

---

## 🔐 Environment & Secrets Management

### Local Development

Create this file:

```

.streamlit/secrets.toml

````

Add:

```toml
API_URL = "https://chatbot-y393.onrender.com/"
````

⚠️ Never commit this file. Add to `.gitignore`:

```
.streamlit/secrets.toml
```

---

## 🚀 Backend Setup (FastAPI)

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Run locally

```bash
uvicorn backend:app --reload
```

Or if uvicorn path fails:

```bash
python -m uvicorn backend:app --reload
```

---

## 💬 `/chat` API Endpoint

### Request

```json
{
  "query": "Hello VenkyAI"
}
```

### Response

```json
{
  "response": "Hello! How can I help you today?"
}
```

---

## 🎨 Frontend Setup (Streamlit)

### Run locally

```bash
streamlit run app.py
```

### API Call Example

```python
import requests
import streamlit as st

API_URL = st.secrets["API_URL"]

response = requests.post(
    f"{API_URL}/chat",
    json={"query": "Hello VenkyAI"},
    timeout=30
)

st.write(response.json())
```

---

## 🌍 Deployment

### ✅ Backend → Render

**Build Command**

```bash
pip install -r requirements.txt
```

**Start Command**

```bash
python -m uvicorn backend:app --host 0.0.0.0 --port 8000
```

**runtime.txt**

```
python-3.12
```

---

### ✅ Frontend → Streamlit Community Cloud

Add this in:

**App Settings → Advanced Settings → Secrets**

```toml
API_URL = "https://chatbot-y393.onrender.com/"
```

---

## 🧠 Future Improvements

* ✅ Multimodal upload
* ✅ Chat history persistence
* ✅ User authentication
* ✅ Admin dashboard
* ✅ Vector DB support (FAISS, Pinecone)

---

## 👨‍💻 Author

**Venkatesh Iyer**
Creator of VenkyAI

---

## ⭐ Support

If you like this project, give it a ⭐ and share it 🚀

````

---


→ Paste → `CTRL + O` → `ENTER` → `CTRL + X`

Then:

```bash
git add README.md
git commit -m "Add VenkyAI README"
git push
```

---


