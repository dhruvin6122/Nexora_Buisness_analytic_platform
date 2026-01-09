# Nexora | AI Business Analytics Agent

![Status](https://img.shields.io/badge/Status-Production-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge)

**Nexora** is an enterprise-grade AI agent capable of translating natural language queries into complex SQL operations, empowering business users to analyze sales, customers, and inventory data instantly.

---

## Overview

In the modern data landscape, valuable business insights are often locked behind complex database schemas, requiring technical expertise (SQL) to access. **Nexora** bridges this gap by serving as an intelligent interface between non-technical stakeholders and enterprise data warehouses.

Nexora is not just a chatbot; it is a **deterministic agent** that understands database schemas, enforces security protocols, and visualizes results dynamically.

## Problem Statement

-   **Dependency on Data Teams**: Business users must wait for analysts to write SQL queries for basic reports.
-   **Static Reporting**: Traditional dashboards are rigid and cannot answer ad-hoc questions ("Why did sales drop yesterday?").
-   **Data Silos**: Critical information (Customers, Orders, Inventory) resides in disconnected tables, making holistic analysis difficult.

## Solution

Nexora solves these challenges by providing:
1.  **Natural Language Interface**: Users ask questions in plain English.
2.  **Real-Time Querying**: The agent constructs and executes SQL against the live database.
3.  **Contextual Awareness**: It understands business logic (e.g., "Best Selling" implies Volume + Revenue).
4.  **Secure Execution**: Read-only access with strict schema validation prevents data corruption.

## System Architecture

The application follows a **Client-Server Architecture**, separating the UI logic from the core reasoning engine.

### Data Flow Overview

1.  **User Interaction**: Business user asks a question on the **Streamlit Frontend**.
2.  **API Gateway**: Frontend sends HTTP request to the **FastAPI Backend**.
3.  **Authentication**: Backend validates request via **Auth Service**.
4.  **Reasoning**: **LangChain Agent** constructs a SQL query using **GPT-4o**.
5.  **Execution**: Agent safely executes the query on the **PostgreSQL Database**.
6.  **Response**: Results are formatted and sent back to the UI for display.

### Core Components

#### 1. Frontend (Streamlit)
-   **Role**: Client-side interface.
-   **Features**: Split-screen login, Real-time chat streaming, Mobile-responsive layout, Dashboard visualization.
-   **Architecture**: Stateless UI that consumes backend APls.

#### 2. Backend (FastAPI)
-   **Role**: Application server and API gateway.
-   **Features**: JWT Authentication, Request Validation (Pydantic), CORS policies, Async handling.
-   **Endpoints**: `/auth`, `/agent`, `/dashboard`.

#### 3. AI Agent Layer (LangChain)
-   **Role**: Reasoning engine.
-   **Capabilities**: SQL Generation, Error Recovery, Hallucination checks, Schema introspection.
-   **Tooling**: Custom `SafeSQLDatabaseTool` for secure execution.

## Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Rapid UI development with Python compatibility |
| **Backend** | FastAPI | High-performance, async web framework |
| **Database** | Neon (PostgreSQL) | Serverless Postgres for scalability |
| **AI Framework** | LangChain | Agent orchestration and tool management |
| **LLM** | OpenAI GPT-4o | State-of-the-art reasoning model |
| **ORM** | SQLAlchemy | Database abstraction and connection pooling |

## Key Features

-   **Autonomous SQL Generation**: Translates questions like "Show me top 5 customers by revenue" into optimized SQL.
-   **Smart Schema Awareness**: Auto-detects ambiguous dates and resolves them based on business context.
-   **Proactive Insights**: Automatically provides analysis alongside raw data tables.
-   **Production Security**: 
    -   Read-Only database permissions.
    -   Input sanitization.
    -   API-level authentication.
-   **Responsive Design**: Fully optimized for Desktop, Tablet, and Mobile browsers.

## Getting Started

### Prerequisites
-   Python 3.10+
-   PostgreSQL Database (Local or Cloud)
-   OpenAI API Key

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/dhruvin6122/Nexora_Buisness_analytic_platform.git
    cd Nexora_Buisness_analytic_platform
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**
    Create a `.env` file in the root directory:
    ```ini
    # Database
    NEON_DATABASE_URL="postgresql://user:password@host/dbname"
    
    # AI Credentials
    OPENAI_API_KEY="sk-..."
    
    # Security (Optional for local)
    SECRET_KEY="your-secret-key"
    ```

### Running the Application

1.  **Start the Backend Server**
    ```bash
    uvicorn backend.main:app --reload --port 8000
    ```
    *The API will be available at `http://localhost:8000`*

2.  **Start the Frontend Client** (In a new terminal)
    ```bash
    streamlit run app.py
    ```
    *The UI will launch at `http://localhost:8501`*

## Deployment

### Cloud Readiness
-   **Backend**: Can be deployed to AWS Lambda (via Mangum), Google Cloud Run, or Railway.
-   **Frontend**: Optimized for Streamlit Cloud or containerized deployment.
-   **Database**: Neon Serverless ensures zero-maintenance scaling.

### Docker Support (Optional)
The application is structured to support multi-container deployment via `docker-compose`.

## Roadmap

-   [ ] **Voice Interface**: Add speech-to-text for hands-free querying.
-   [ ] **Multi-Database Support**: Connect to Snowflake and BigQuery.
-   [ ] **Advanced Visualization**: Auto-generate Plotly charts based on result data types.
-   [ ] **Role-Based Access Control (RBAC)**: Granular permissions for different business units.

## Contributing

Contributions are welcome! Please follow these steps:
1.  Fork the project.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Author

**Dhruvin Patel**  
*AI Engineer & Full Stack Developer*
