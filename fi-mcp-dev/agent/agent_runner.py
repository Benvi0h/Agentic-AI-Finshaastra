import requests
from analyzer import analyze_transactions

def fetch_transactions():
    url = "http://localhost:8080/mcp/stream"
    headers = {
        "Content-Type": "application/json",
        "Mcp-Session-Id": "mcp-session-594e48ea-fea1-40ef-8c52-7552dd9272af"
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

    response = requests.post(url, headers=headers, json=payload)
    print("pp", response.text)

    return response.text

def run_agent():
    raw_json = fetch_transactions()
    result = analyze_transactions(raw_json)

    if "error" in result:
        print("Error:", result["error"])
    else:
        print("\n💰 Income & Emergency Fund Analysis")
        print(f"Total Income (2 months): ₹{result['total_income']}")
        print(f"Avg Monthly Expense     : ₹{result['monthly_expense']}")
        print(f"Emergency Fund Available: ₹{result['emergency_fund']}")
        print(f"Coverage Duration       : {result['months_covered']} months")
        print(f"Stability               : {result['status']}")

if __name__ == "__main__":
    run_agent()
