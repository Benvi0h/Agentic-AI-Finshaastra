# import json
# import requests

# # from google.adk.agents.llm_agent import Agent
# from google.adk.agents import Agent
# from prompt import FINANCE_PROMPT
# from analyzer import analyze_transactions

# # Agent configuration
# MCP_SESSION_ID = "mcp-session-594e48ea-fea1-40ef-8c52-7552dd9272af"
# MCP_URL = "http://localhost:8080/mcp/stream"

# finance_agent = Agent(
#     model="gemini-2.0-flash",
#     name="FinanceAgent",
#     instruction=FINANCE_PROMPT,
#     tools=[]  # No toolset needed for local MCP call
# )

# def fetch_transactions():
#     headers = {
#         "Content-Type": "application/json",
#         "Mcp-Session-Id": MCP_SESSION_ID
#     }

#     payload = {
#         "jsonrpc": "2.0",
#         "id": 1,
#         "method": "tools/call",
#         "params": {
#             "name": "fetch_bank_transactions",
#             "arguments": {}
#         }
#     }

#     response = requests.post(MCP_URL, headers=headers, json=payload)
#     response.raise_for_status()
#     return response.text

# def main():
#     print("🤖 Agent starting...")

#     try:
#         raw_data = fetch_transactions()
#         print("✅ Data fetched successfully.")

#         result = analyze_transactions(raw_data)

#         if "error" in result:
#             print("❌ Analysis Error:", result["error"])
#             return

#         # Compose message to pass to agent LLM
#         message = (
#             f"💰 Income & Emergency Fund Summary\n"
#             f"Total Income (2 months): ₹{result['total_income']}\n"
#             f"Avg Monthly Expense     : ₹{result['monthly_expense']}\n"
#             f"Emergency Fund Available: ₹{result['emergency_fund']}\n"
#             f"Coverage Duration       : {result['months_covered']} months\n"
#             f"Stability               : {result['status']}"
#         )

#         print("\n📢 Agent LLM Summary:")
#         finance_agent(message)

#     except Exception as e:
#         print("❌ Agent failed:", e)

# if __name__ == "__main__":
#     main()

#working file
import os
import json
import requests
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio # Still needed for asyncio.run(async_main()) if other parts of your flow become async

from google.adk.agents import Agent # Keep this if you plan to use ADK features later
from prompt import FINANCE_PROMPT
from analyzer import analyze_transactions

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
MCP_SESSION_ID = os.getenv("MCP_SESSION_ID")
MCP_URL = os.getenv("MCP_URL")

# Explicit Gemini configuration
genai.configure(api_key=API_KEY)

# Define the model name separately
MODEL_NAME = "gemini-2.0-flash"

# Create Finance Agent (if you intend to use its ADK features)
finance_agent = Agent(
    model=MODEL_NAME,
    name="FinanceAgent",
    instruction=FINANCE_PROMPT,
    tools=[]
)

# Create a separate GenerativeModel instance for direct LLM calls
gemini_model = genai.GenerativeModel(MODEL_NAME)


def fetch_transactions():
    headers = {
        "Content-Type": "application/json",
        "Mcp-Session-Id": MCP_SESSION_ID
    }

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "fetch_bank_transactions",
            "arguments": {}
        }
    }

    response = requests.post(MCP_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.text

async def async_main(): # Keep this as async because asyncio.run() needs an awaitable.
                        # It doesn't mean functions *inside* it must be awaited,
                        # only if they themselves are async.
    print("🤖 Agent starting...")

    try:
        raw_data = fetch_transactions()
        print("✅ Data fetched successfully.")

        analysis_result = analyze_transactions(raw_data)

        if "error" in analysis_result:
            print("❌ Analysis Error:", analysis_result["error"])
            return

        message_data = (
            f"💰 Income & Emergency Fund Summary\n"
            f"Total Income (2 months): ₹{analysis_result['total_income']}\n"
            f"Avg Monthly Expense     : ₹{analysis_result['monthly_expense']}\n"
            f"Emergency Fund Available: ₹{analysis_result['emergency_fund']}\n"
            f"Coverage Duration       : {analysis_result['months_covered']} months\n"
            f"Stability               : {analysis_result['status']}"
        )

        print("\n📢 Agent LLM Summary:")

        # Construct the full prompt including the agent's instruction and the data
        full_prompt_for_llm = f"{FINANCE_PROMPT}\n\nHere is the financial data:\n{message_data}"

        print(f"Sending prompt to LLM:\n{full_prompt_for_llm}\n")

        # ✅ REMOVE 'await' here!
        llm_response = gemini_model.generate_content(full_prompt_for_llm)

        # Print the LLM's response
        print("\nFinal LLM Output:")
        # Check if the response has text content
        if hasattr(llm_response, 'text'):
            print(llm_response.text)
        else:
            print("LLM response did not have a 'text' attribute. Full response object:")
            print(llm_response)


    except Exception as e:
        print(f"❌ Agent failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    # asyncio.run() expects an awaitable, so we still define async_main and run it.
    # The functions *inside* async_main don't have to be async unless they truly are.
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
# import os
# import json
# import requests
# from google.adk.agents import Agent
# from prompt import FINANCE_PROMPT
# from analyzer import analyze_transactions
# import google.generativeai as genai

# # Agent configuration
# MCP_SESSION_ID = os.getenv("MCP_SESSION_ID")
# MCP_URL = os.getenv("MCP_URL")
# API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=API_KEY)

# # Function to fetch transactions from MCP
# def fetch_bank_transactions():
#     headers = {
#         "Content-Type": "application/json",
#         "Mcp-Session-Id": MCP_SESSION_ID,
#     }
#     payload = {
#         "jsonrpc": "2.0",
#         "id": 1,
#         "method": "tools/call",
#         "params": {
#             "name": "fetch_bank_transactions",
#             "arguments": {}
#         }
#     }

#     try:
#         response = requests.post(MCP_URL, headers=headers, json=payload)
#         response.raise_for_status()
#         result = response.json().get("result", {}).get("result", [])
#         return result
#     except Exception as e:
#         print(f"❌ Failed to fetch transactions: {e}")
#         return []

# # Core function to run the financial agent with user input
# def run_financial_agent(user_message: str):
#     # Step 1: Fetch and analyze transactions
#     transactions = fetch_bank_transactions()
#     if not transactions:
#         return "⚠️ Could not fetch transaction data. Please try again later."

#     analysis = analyze_transactions(transactions)

#     # Step 2: Prepare context for the agent
#     context = {
#         "user_question": user_message,
#         "transaction_insights": analysis
#     }

#     # Step 3: Initialize agent
#     finance_agent = Agent(
#         model="gemini-2.0-flash",
#         name="FinanceAgent",
#         instruction=FINANCE_PROMPT,
#         tools=[]
#     )

#     # Step 4: Run the agent
#     try:
#         response = finance_agent.run(context)
#         return response if response else "⚠️ No response generated by the agent."
#     except Exception as e:
#         print(f"❌ Agent execution failed: {e}")
#         return "❌ Agent execution failed."

