# HackLens Backend

HackLens is a lightweight, AI-powered backend system designed to review and evaluate computer science content, including code snippets, programming notes, technical documentation, and `.docx` files.

## Project Structure

```text
backend/
 ├── app/
 │    ├── main.py                     # Entry point of the FastAPI application
 │    ├── routes/
 │    │     └── analyze.py            # API endpoint router for code/document analysis
 │    ├── services/
 │    │     ├── llm_service.py        # Communicates with the Groq LLM API
 │    │     ├── file_parser.py        # Extracts text from uploaded files (e.g., .docx)
 │    │     └── prompt_builder.py     # Constructs prompts for the evaluation tasks
 │    └── models/
 │          └── request_models.py     # Pydantic schemas for request validation & response mapping
 │
 ├── requirements.txt                 # Backend dependency list
 ├── .env                             # Local environment variables
 └── README.md                        # Documentation
```

## Setup Instructions

1. **Setup Virtual Environment:**
   If `.venv` is not already configured, create it:
   ```bash
   python -m venv .venv
   ```

2. **Activate Virtual Environment:**
   - On Windows (PowerShell):
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - On Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Rename or edit `.env` and fill in your `GROQ_API_KEY`:
   ```env
   GROQ_API_KEY=your-actual-api-key
   ```

5. **Run the Application:**
   ```bash
   uvicorn app.main:app --reload
   ```
