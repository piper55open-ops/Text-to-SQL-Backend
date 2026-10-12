# Intelligent Text-to-SQL AI Agent

A **Flask-based Text-to-SQL prototype** that lets users explore a PostgreSQL database using natural-language questions. The application passes database schema information to **Google Gemini**, checks the generated SQL, and returns query results through a simple web interface.

> **Project status:** A local development and learning project. It is not intended for production use without further security hardening.

## Features

- **Natural-language queries:** Convert user questions into PostgreSQL SQL with the Google Gen AI SDK.
- **Schema-aware generation:** Read table and column metadata from PostgreSQL's `information_schema` to provide context to the model.
- **Two layers of query protection:** Apply a basic SQL keyword filter and execute queries through an `agent_runner` database role with read-only permissions.
- **Web interface and API:** Connect a vanilla JavaScript frontend to Flask's `/api/chat` endpoint.
- **Automated API tests:** Use `pytest` and mocking to check health and input-validation behavior without calling Gemini or the database.

## Tech Stack

| Component | Technology |
| --- | --- |
| Backend | Python, Flask |
| AI | Google Gen AI SDK (`google-genai`) |
| Database | PostgreSQL, `psycopg2` |
| Frontend | HTML, CSS, vanilla JavaScript, Marked.js |
| Testing | `pytest`, `unittest.mock` |

## How It Works

```text
Natural-language question
          |
          v
     Flask /api/chat
          |
          v
Read PostgreSQL schema metadata
          |
          v
   Gemini generates SQL
          |
          v
  Basic SQL safety check
          |
          v
PostgreSQL query (agent_runner)
          |
          v
Results returned to the browser
```

Schema metadata is used as prompt context; this project does **not** currently implement a vector database or a full retrieval-augmented generation (RAG) pipeline.

## Getting Started

### 1. Prerequisites

- Python **3.10+**
- PostgreSQL running locally (the scripts expect port `5432`)
- A Gemini API key
- A local development database; **do not use production data**

### 2. Clone the repository

```bash
git clone https://github.com/piper55open-ops/text-to-sql-agent.git
cd text-to-sql-agent
```

### 3. Install dependencies

Create and activate a virtual environment. For **Windows PowerShell**:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install flask psycopg2-binary python-dotenv google-genai pytest
```

The repository does not yet include a finalized `requirements.txt`; the command above lists the libraries used by the prototype and its tests.

### 4. Configure Gemini and PostgreSQL

Create a `.env` file in the project root:

```dotenv
GEMINI_API_KEY=replace_with_your_gemini_api_key
```

**Database configuration:** The current prototype still has local PostgreSQL connection settings in several Python scripts and, where present, `docker-compose.yml`. Make sure the database name, accounts, and passwords match your local PostgreSQL setup before proceeding. Database credentials should be moved to environment variables before deployment.

The example database is named `enterprise_data`. You can start PostgreSQL locally or use the project's Docker Compose configuration if it is included in your checkout.

### 5. Initialize sample data and read-only access

From the project root, run the scripts in this order:

```bash
python dp_setup.py
python seed_data.py
python setup_security.py
```

- `dp_setup.py` creates the sample tables.
- `seed_data.py` inserts example records. **Warning:** It clears existing data in the sample tables; run it only against a disposable development database.
- `setup_security.py` creates/configures the `agent_runner` role and grants read-only table access.

### 6. Start the application

```bash
python server.py
```

Open **http://127.0.0.1:5000** in your browser.

## API

**`POST /api/chat`** accepts a JSON question:

```json
{
  "question": "How many users are there?"
}
```

For a successful request, the API returns an `answer` field containing the formatted result. Invalid or missing questions should return HTTP `400`.

**`GET /health`** is used for a basic health check in the development version.

## Run Tests

```bash
python -m pytest -v
```

The current tests focus on Flask API behavior such as health checks, empty/whitespace inputs, trimming questions, and rejecting non-string values. They use mocks rather than validating live Gemini responses or database queries.

## Project Structure

```text
app/
  agent_core.py         # Gemini request, SQL generation, query execution
  metadata_provider.py  # PostgreSQL schema inspection
  security.py           # Basic SQL keyword checks
static/
  index.html            # Browser UI
tests/
  test_health.py        # Flask API tests
server.py               # Flask application and routes
dp_setup.py             # Sample table creation
seed_data.py            # Demo records (destructive to existing sample data)
setup_security.py       # Read-only database role configuration
README.md
```

## Security and Limitations

This project demonstrates security-conscious design, **not a production-grade SQL sandbox**:

- The regex-based keyword filter is a preliminary check and may miss unsafe SQL. Database permissions remain essential.
- The application currently needs stronger SQL parsing/allowlisting, frontend output sanitization, and more complete error handling and tests.
- Keep `.env`, API keys, and database passwords out of Git. Rotate any credentials that were previously committed or shared.
- Review all local credentials, Flask debug settings, and access controls before making the application publicly accessible.

## Demo

![Text-to-SQL web interface](https://github.com/user-attachments/assets/7a47dbf2-e836-40ed-a573-66cd8db656cd)
