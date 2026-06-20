# HackLens 🔍

### AI-Powered Technical Evaluator for Computer Science Content

HackLens is a lightweight AI-powered backend application that reviews and evaluates computer science–related content such as code snippets, technical notes, documentation, and `.docx` files.

The system leverages Large Language Models (LLMs) to provide structured feedback, helping users identify strengths, weaknesses, and potential improvements in their technical content.

---

## 🚀 Features

### 📄 Technical Content Analysis

HackLens can evaluate:

* Source code snippets
* Programming assignments
* Technical notes
* Documentation
* `.docx` files containing technical content

### 📊 Structured Evaluation

The system generates:

* Overall evaluation score
* Strengths
* Weaknesses
* Actionable suggestions

### 🧠 AI-Powered Review

The analysis is performed using a Large Language Model (LLM) integrated through the Groq API.

### 📁 Document Upload Support

Users can upload `.docx` files directly for evaluation.

### ⚡ FastAPI Backend

Built using FastAPI for high performance and easy API integration.

---

## 🏗️ Project Architecture

```text
User Input
    │
    ├── Code Snippet
    ├── Technical Notes
    └── .docx File
            │
            ▼
      FastAPI Backend
            │
            ▼
      File Parser
            │
            ▼
      Prompt Builder
            │
            ▼
         Groq API
            │
            ▼
     AI Evaluation Engine
            │
            ▼
      Structured Response
```

---

## 🛠️ Tech Stack

### Backend

* FastAPI
* Python

### AI

* Groq API
* Llama Models

### Document Processing

* python-docx

### Development Tools

* Uvicorn
* Pydantic
* Python Dotenv

---

## 📂 Project Structure

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   └── analyze.py
│   │
│   ├── services/
│   │   ├── file_parser.py
│   │   ├── prompt_builder.py
│   │   └── llm_service.py
│   │
│   └── models/
│       └── request_models.py
│
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone <repository-url>
cd HackLens/backend
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## ▶️ Running the Server

From the backend directory:

```bash
uvicorn app.main:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 📬 API Endpoint

### Analyze Content

**POST**

```http
/api/v1/analyze
```

Supports:

* Text input
* `.docx` file upload

---

### Example Input

```text
Content:
def add(a, b):
    return a + b

Content Type:
code
```

---

### Example Response

```json
{
  "evaluation_score": 8.5,
  "strengths": [
    "Readable and concise implementation"
  ],
  "weaknesses": [
    "Missing type hints and documentation"
  ],
  "suggestions": [
    "Add function docstrings",
    "Use type annotations"
  ]
}
```

---

## 🎯 Use Cases

* Code review assistance
* Programming assignment evaluation
* Technical documentation review
* Student project assessment
* Learning and self-improvement

---

## 🔮 Future Enhancements

* Frontend Web Interface
* Database Integration
* User History Tracking
* PDF Support
* Multi-Language Code Evaluation
* Advanced Scoring Metrics
* Export Reports

---

## 📌 Project Status

Current Version: **MVP Backend**

Implemented:

* FastAPI Backend
* Content Upload
* DOCX Parsing
* Prompt Generation
* AI Evaluation Pipeline
* Structured JSON Responses

Planned:

* Frontend Application
* Database Integration
* Deployment

---

## 👨‍💻 Team

Developed as part of an AI-powered technical evaluation project.

---

### HackLens

**"Review. Analyze. Improve."**
