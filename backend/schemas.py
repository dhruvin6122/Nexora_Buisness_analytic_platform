from pydantic import BaseModel
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime

# --- Auth Models ---
class UserSignup(BaseModel):
    full_name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str  # Send as string to avoid serialization issues
    full_name: str
    email: str
    # created_at: datetime # Optional to include

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None

class SaveMessageRequest(BaseModel):
    user_id: str
    role: str
    content: str

# --- Agent Models ---
class ChatRequest(BaseModel):
    input: str
    user_id: str
    history: List[dict] # List of {"role": "...", "content": "..."}

class ChatResponse(BaseModel):
    output: str

# --- Dashboard Models ---
class DashboardStats(BaseModel):
    today_orders: int
    today_revenue: float
    total_customers: int
