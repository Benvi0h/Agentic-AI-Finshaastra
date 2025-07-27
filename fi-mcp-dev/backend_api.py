from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import asyncio
from agent.agent import async_main as agent_async_main

app = FastAPI()

# Allow CORS for frontend localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust if frontend runs on different port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

def invoke_agent(message: str) -> str:
    # For now, ignore the message and run the agent's async_main to get response
    # This is a blocking call to run the async function synchronously
    try:
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.get_event_loop().run_until_complete(agent_async_main())
        # The agent_async_main currently prints output, so we need to capture it or refactor agent.py to return string
        # For now, return a placeholder response
        return "Agent processed the message. (Response capture not implemented yet)"
    except Exception as e:
        return f"Agent failed: {e}"

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    user_message = chat_request.message
    response_text = invoke_agent(user_message)
    return {"response": response_text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
