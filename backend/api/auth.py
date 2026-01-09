from fastapi import APIRouter, HTTPException, Depends
from backend.auth.service import AuthService
from backend.schemas import UserSignup, UserLogin, UserResponse, SaveMessageRequest, ChatMessage
from typing import List, Optional

router = APIRouter()

def get_auth_service():
    return AuthService()

@router.post("/signup", response_model=UserResponse)
def signup(user_data: UserSignup, auth: AuthService = Depends(get_auth_service)):
    user, error = auth.signup(user_data.full_name, user_data.email, user_data.password)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return UserResponse(id=str(user.id), full_name=user.full_name, email=user.email)

@router.post("/login", response_model=UserResponse)
def login(user_data: UserLogin, auth: AuthService = Depends(get_auth_service)):
    user, error = auth.login(user_data.email, user_data.password)
    if error:
        raise HTTPException(status_code=401, detail=error)
    return UserResponse(id=str(user.id), full_name=user.full_name, email=user.email)

@router.get("/history/{user_id}", response_model=List[ChatMessage])
def get_history(user_id: str, limit: Optional[int] = None, auth: AuthService = Depends(get_auth_service)):
    try:
        messages = auth.get_chat_history(user_id, limit=limit)
        return [ChatMessage(role=m.role, content=m.content, timestamp=m.timestamp) for m in messages]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/message")
def save_message(request: SaveMessageRequest, auth: AuthService = Depends(get_auth_service)):
    try:
        auth.save_message(request.user_id, request.role, request.content)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
