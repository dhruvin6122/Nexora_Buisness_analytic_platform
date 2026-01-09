from fastapi import APIRouter, HTTPException
from backend.agent import get_agent_executor
from backend.schemas import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        # Convert Pydantic models to dict/tuple format expected by agent
        history_tuples = [(msg['role'], msg['content']) for msg in request.history]
        
        agent = get_agent_executor(chat_history=history_tuples)
        response = agent.invoke({"input": request.input})
        return ChatResponse(output=response["output"])
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
