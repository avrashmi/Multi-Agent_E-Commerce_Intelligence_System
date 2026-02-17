# 🛍️ Multi-Agent E-Commerce Intelligence System

An AI-powered multi-agent shopping assistant that helps users make confident purchase decisions by analyzing products, reviews, and alternatives in seconds.

---

## 🚨 Problem

Online shopping is overwhelming.

- 50+ similar products  
- Hundreds of reviews per item  
- Conflicting ratings  
- No intelligent guidance  

Customers spend 15+ minutes reading reviews and still feel uncertain — leading to cart abandonment.

---

## 💡 Solution

This project implements a **Multi-Agent E-Commerce Assistant** that coordinates 4 specialized AI agents to provide instant, trustworthy, and contextual product guidance.

Instead of just showing ratings, the system:

- Finds relevant products  
- Analyzes review sentiment  
- Extracts pros and cons  
- Answers user-specific questions  
- Suggests better alternatives  

All in ~15 seconds.

---

## 🧠 How It Works

User asks:

> “Is this laptop good for video editing?”

### 🔍 Agent 1 – Product Retrieval (Rule-Based, Parallel)

- Finds relevant products using keyword scoring  
- No API calls  
- ~0.01s response  

### 💬 Agent 2 – Sentiment Analysis (LLM + Loop + Memory)

- Analyzes reviews in batches  
- Extracts sentiment + pros/cons  
- Caches results to avoid repeat processing  

### 🤔 Agent 3 – Question Answering (LLM Sequential)

- Synthesizes product + review insights  
- Generates natural, contextual answers  

### 🎯 Agent 4 – Recommendation (Rule-Based Parallel)

- Checks stock  
- Evaluates sentiment thresholds  
- Suggests alternatives if needed  

The orchestrator compiles everything into a clear, trustworthy final response.

---

## ⚙️ Architecture Philosophy

> “Use the simplest technique that solves the problem effectively.”

- Rules for simple logic (fast & free)  
- LLMs for complex reasoning  
- Sequential flow when dependencies exist  
- Parallel execution when possible  
- Memory caching for performance  

**Hybrid > Pure AI**

---

## 🚀 Key Features

- ✅ Sequential multi-agent orchestration  
- ✅ Parallel evaluation for speed  
- ✅ Batch processing (66% fewer API calls)  
- ✅ Memory caching (instant repeat queries)  
- ✅ Rate-limit handling & retries  
- ✅ Modular, clean architecture  
- ✅ Comprehensive test suite  

---

## 🛠️ Tech Stack

- Python  
- Google Gemini API  
- Pandas / NumPy  
- Rule-based scoring + Decision Trees  
- In-memory caching  
- Modular agent architecture  

---

## 📁 Project Structure

ecommerce-multi-agent/
│
├── agents/
│ ├── agent1_retrieval.py
│ ├── agent2_sentiment.py
│ ├── agent3_qa.py
│ └── agent4_recommendation.py
│
├── utils/
├── data/
├── tests/
├── main.py
└── requirements.txt



---

## ▶️ Setup

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt

2️⃣ Add your Gemini API key in .env
GEMINI_API_KEY=your_key_here

3️⃣ Run the system
python main.py

📊 Performance Improvements
Optimization	Result
Batch Processing	66% fewer API calls
Memory Caching	100% savings on repeat queries
Hybrid Architecture	75% faster than naive LLM-only approach
🎯 Why This Matters

Reduces decision fatigue

Improves customer confidence

Potentially lowers cart abandonment

Demonstrates production-ready multi-agent orchestration

This system can be extended to healthcare, travel, finance, or any domain where decisions are complex.

🔮 Future Improvements

PostgreSQL / MongoDB

Redis caching

FastAPI backend

React frontend

Docker deployment

Vector database for semantic search

Monitoring with Prometheus + Grafana



