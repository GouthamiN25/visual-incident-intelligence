# 🛡️ Visual Incident Intelligence

**Turn screenshots, sketches, and diagrams into instant incident insights using multimodal AI and vector search.**

---

## 🏆 Hackathon
**Sketch & Search Hackathon**  
https://sketchandsearch.dev/

---

## 🚀 Overview

Visual Incident Intelligence is an AI-powered system that enables teams to **search and reason over visual incident evidence** such as:

- Monitoring dashboard screenshots (Splunk, Datadog, Grafana)
- Hand-drawn or whiteboard network sketches
- Cloud and system architecture diagrams

Instead of treating these visuals as static images, the system converts them into **semantic representations** and retrieves **similar historical incidents** using vector search.

This helps security, SRE, and DevOps teams respond faster by reusing knowledge from past incidents.

---

## ❓ Problem Statement

During real-world incidents, teams frequently share:
- Screenshots of dashboards
- Photos of whiteboard sketches
- Architecture diagrams with highlighted failures

However:
- These visuals are **not searchable**
- Teams cannot easily compare them with past incidents
- Valuable incident knowledge remains siloed or lost

This slows down triage and increases Mean Time To Resolution (MTTR).

---

## ✅ Solution

Visual Incident Intelligence transforms visual artifacts into **searchable incident intelligence** by:

1. Understanding images using **multimodal AI**
2. Extracting structured incident signals
3. Converting signals into vector embeddings
4. Using **semantic vector search** to find similar incidents
5. Returning **explainable matches and suggested actions**

---

## 🧠 How It Works (Architecture)

### 1️⃣ Input
User uploads:
- Dashboard screenshot
- Network sketch
- Architecture diagram  
(Optional) Adds a short textual note for context

---

### 2️⃣ Multimodal Understanding
- **Gemini Vision** analyzes the image
- Extracts:
  - Asset type (dashboard / network / architecture)
  - Entities (services, components, protocols)
  - Symptoms and indicators
  - Severity estimate

---

### 3️⃣ Embedding & Storage
- Extracted signals are converted into embeddings using **Sentence Transformers**
- Stored in **Qdrant vector database** with metadata

---

### 4️⃣ Semantic Search
- New incidents are compared against historical incidents
- Search is based on **semantic similarity**, not keywords

---

### 5️⃣ Output
The system returns:
- Top similar incidents with similarity scores
- Explanation of why incidents match
- Suggested investigation and remediation steps

---

## 🔍 Why This Fits “Sketch & Search”

**Sketch & Search** is about turning **visual inputs** into **searchable intelligence** using embeddings and vector search.

This project directly aligns by:
- Treating sketches, screenshots, and diagrams as the “sketch”
- Converting visual meaning into embeddings
- Using Qdrant to perform semantic search
- Returning transparent, explainable results

> We search incidents by **what the image means**, not by filenames or tags.

---

## 🖥️ User Interface Overview

The web interface allows users to:

- Upload an incident-related image
- Add optional context notes
- Seed demo incidents for realistic search results
- View:
  - System and Qdrant health status
  - Matched incidents with confidence scores
  - Suggested actions

This is a **live backend-connected demo**, not a mock UI.

---

## 🎬 Demo Flow

1. Start the application
2. Click **Seed Demo Incidents**
3. Upload a screenshot, sketch, or diagram
4. Click **Analyze & Match**
5. Review:
   - Similar incidents
   - Risk explanation
   - Suggested actions

---

## 🧰 Tech Stack

### Backend
- **FastAPI** – API server
- **Google Gemini Vision** – multimodal image understanding
- **Sentence Transformers** – embeddings
- **Qdrant** – vector database

### Frontend
- **HTML + Tailwind CSS**
- **Vanilla JavaScript**

---

## 📦 Project Structure
visual-incident-intelligence/
├── app/
│ ├── main.py
│ ├── vision.py
│ ├── embedder.py
│ ├── qdrant_store.py
│ ├── scoring.py
│ ├── storage.py
│ └── schemas.py
│
├── ui/
│ └── index.html
│
├── data/
│ └── uploads/
│
├── requirements.txt
├── .gitignore
└── README.md

## 🏆 Use Cases

Security Operations (SOC)

Incident Response Teams

SRE / DevOps

Cloud Platform Operations

Enterprise IT Monitoring

## 📈 Impact

Faster incident triage

Reuse of historical incident knowledge

Reduced MTTR

Better decision-making under pressure

## 🔮 Future Improvements

Full production-grade Gemini Vision extraction

Incident report export (PDF / ticket)

Role-based access control

Timeline-based incident correlation

Integration with monitoring tools (Splunk, Datadog)

## ⚠️ Disclaimer
This project is intended solely for educational, research, and hackathon demonstration purposes.
It does not provide financial advice, security guarantees, or production-grade fraud assessment.

Any insights or outputs generated should not be used for real-world financial decision-making or business operations.
The author assumes no liability for misuse, misinterpretation, or unauthorized use of the project.

## 👩‍💻 Author

Gouthami Nadupuri
Data Scientist | AI Engineer

GitHub: https://github.com/GouthamiN25

LinkedIn: https://www.linkedin.com/in/gouthami-nadupuri

