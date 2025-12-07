from fastapi import FastAPI,HTTPException
from service import ChatService,ChatResponse,ChatRequest
from icecream import ic


# Initialize FastAPI app
app = FastAPI(title="Chat Service API")

chat_service = ChatService()


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Chat Service API is running", "status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that accepts a query and returns the LLM response.
    
    Args:
        request: ChatRequest with query field
        
    Returns:
        ChatResponse with query, answer, and response_time
    """
    try:
        # Call the chat service with the query
        result = chat_service.query_chat(query=request.query)
        return ChatResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        ic("Unexpected error in chat endpoint")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "chat"}


