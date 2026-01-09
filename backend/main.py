from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import auth, agent, dashboard
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Nexora Analytics API", version="1.0.0")

# CORS Configuration
origins = [
    "http://localhost:8501",  # Streamlit default port
    "http://127.0.0.1:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(agent.router, prefix="/agent", tags=["Agent"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Nexora API is running"}
