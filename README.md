#Intelligent Text-to-SQL AI Agent

An enterprise-grade Text-to-SQL engine built with **Flask**, **PostgreSQL**, and **Google Gemini 3.1 Pro SDK**. This project demonstrates a complete AI-driven data retrieval pipeline with a strong emphasis on **Security Architecture** and **RAG (Retrieval-Augmented Generation)** principles.

###Key Features

* **Natural Language Interaction**: Translates complex human questions into precise PostgreSQL queries using the Gemini 3.1 Flash Preview model.
* **Context-Aware Schema Injection**: Dynamically retrieves database metadata (Schema) to provide AI with high-fidelity context, minimizing hallucinations.
* **Dual-Layer Security Shield**:
    * **Logic Layer**: Regex-based SQL interceptor to block destructive commands (`DROP`, `DELETE`, `UPDATE`, etc.).
    * **Physical Layer**: Implements **RBAC (Role-Based Access Control)** using a restricted `agent_runner` database account with strictly read-only permissions.
* **Decoupled Architecture**: A clean, industry-standard Frontend-Backend separation using a Flask RESTful API and vanilla JavaScript.

###Tech Stack

* **Backend**: Python, Flask
* **AI Engine**: Google GenAI SDK (Gemini 3.1 Flash Preview)
* **Database**: PostgreSQL (`psycopg2`)
* **Frontend**: HTML5, CSS3, Vanilla JavaScript (Fetch API, Marked.js)
* 
Prerequisites:
Python 3.9+
PostgreSQL installed and running locally on default port 5432.

###Getting Started

**1. Clone the Repository**
git clone [https://github.com/piper55open-ops/text-to-sql-agent.git](https://github.com/piper55open-ops/text-to-sql-agent.git)
cd text-to-sql-agent

2. Configure Environment
Create a .env file in the root directory:
GEMINI_API_KEY=your_google_api_key_here

3. Setup Database
Run the setup scripts provided to initialize tables and seed local testing data:
python app/db_setup.py
python seed_data.py

5. Run the Application
python server.py
Access the UI at http://127.0.0.1:5000.

<img width="869" height="737" alt="5cf3d2b0969f4f0f5178bf30fbc4a07" src="https://github.com/user-attachments/assets/7a47dbf2-e836-40ed-a573-66cd8db656cd" />

