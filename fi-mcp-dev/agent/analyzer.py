# import json

# def analyze_transactions(raw_json):
#     try:
#         text_data = json.loads(raw_json)["result"]["content"][0]["text"]
#         data = json.loads(text_data)

#         income = 0
#         expenses = 0
#         balances = []

#         for bank in data["bankTransactions"]:
#             for txn in bank["txns"]:
#                 amount = float(txn[0])
#                 txn_type = txn[3]
#                 current_balance = float(txn[5])
#                 balances.append(current_balance)

#                 if txn_type == 1:  # CREDIT
#                     income += amount
#                 elif txn_type == 2:  # DEBIT
#                     expenses += amount

#         avg_monthly_expense = expenses / 2  # assuming 2 months of data
#         emergency_fund = max(balances)
#         months_covered = round(emergency_fund / avg_monthly_expense, 2) if avg_monthly_expense else 0

#         return {
#             "total_income": income,
#             "monthly_expense": avg_monthly_expense,
#             "emergency_fund": emergency_fund,
#             "months_covered": months_covered,
#             "status": "🟢 Stable" if months_covered >= 3 else "🟡 Caution" if months_covered >= 1 else "🔴 Low"
#         }

#     except Exception as e:
#         return {"error": str(e)}
import json

def analyze_transactions(raw_json):
    try:
        text_data = json.loads(raw_json)["result"]["content"][0]["text"]
        data = json.loads(text_data)

        income = 0
        expenses = 0
        balances = []

        for bank in data["bankTransactions"]:
            for txn in bank["txns"]:
                amount = float(txn[0])
                txn_type = txn[3]
                current_balance = float(txn[5])
                balances.append(current_balance)

                if txn_type == 1:  # CREDIT
                    income += amount
                elif txn_type == 2:  # DEBIT
                    expenses += amount

        avg_monthly_expense = expenses / 2  # assume 2 months of data
        emergency_fund = max(balances)
        months_covered = round(emergency_fund / avg_monthly_expense, 2) if avg_monthly_expense else 0

        return {
            "total_income": income,
            "monthly_expense": avg_monthly_expense,
            "emergency_fund": emergency_fund,
            "months_covered": months_covered,
            "status": (
                "🟢 Stable" if months_covered >= 3
                else "🟡 Caution" if months_covered >= 1
                else "🔴 Low"
            )
        }

    except Exception as e:
        return {"error": str(e)}
