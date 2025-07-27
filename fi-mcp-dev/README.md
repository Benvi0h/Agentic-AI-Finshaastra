# Fi-MCP Project

## Overview
Fi-MCP is a financial management platform that integrates AI-powered agents to assist users with financial planning, budgeting, debt management, and savings analysis. The project consists of:

- **Agent Folder**: Contains individual Python agents responsible for various financial tasks such as tax saving, debt repayment, and transaction analysis.
- **Backend API**: A FastAPI service that exposes endpoints to interact with the agents and serves as a bridge between the frontend and the Python agents.
- **Frontend (Finshaastra)**: A Next.js React application that provides a chat interface for users to interact with the AI financial assistant.

## Project Structure
```
fi-mcp-dev/
├── agent/                  # Python agents and related modules
│   ├── agent.py            # Main agent logic and LLM integration
│   ├── agent_runner.py     # Script to run agents standalone
│   ├── analyzer.py         # Transaction analysis utilities
│   ├── agent_tax_saving.py # Tax saving agent
│   ├── agent_debt_rep.py   # Debt repayment agent
│   ├── prompt.py           # Prompts for agents
│   └── ...                 # Other agent-related files
├── backend_api.py          # FastAPI backend service exposing /chat endpoint
├── Finshaastra/            # Frontend Next.js app
│   └── app/
│       └── chat/
│           └── page.tsx    # Chat UI component
├── README.md               # This file
├── go.mod                  # Go module file (if applicable)
└── ...
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- Google API key for Gemini LLM (set in environment variables)

### Backend Setup
1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
3. Install required Python packages:
   ```bash
   pip install fastapi uvicorn requests python-dotenv google-generativeai
   ```
4. Set environment variables in a `.env` file in `fi-mcp-dev/`:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   MCP_SESSION_ID=your_mcp_session_id_here
   MCP_URL=http://localhost:8080/mcp/stream
   ```
5. Run the backend API server:
   ```bash
   python backend_api.py
   ```
   The backend will be available at `http://localhost:5000`.

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd client
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
4. Open your browser and go to `http://localhost:3000/chat` to access the chat interface.

## Usage
- Use the chat interface to send financial queries.
- The frontend sends messages to the backend `/chat` endpoint.
- The backend invokes the appropriate Python agent to process the message and returns a response.
- Responses are displayed in the chat UI with optional charts and insights.

## Extending the Project
- Add new agents in the `agent/` folder.
- Update `backend_api.py` to route messages to different agents based on user input.
- Enhance the frontend chat UI with more features and better visualizations.

## Troubleshooting
- Ensure all environment variables are correctly set.
- Verify backend is running on port 5000.
- Check that the MCP service is running and accessible at the configured MCP_URL.
- Review logs for errors in both backend and frontend terminals.

