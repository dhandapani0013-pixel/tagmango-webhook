
from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import json

app = Flask(__name__)

# Google Sheets authentication
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# --------------------------------------------------
# LOCAL + RENDER GOOGLE CREDENTIALS
# --------------------------------------------------

service_account_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")

if service_account_json:
    # Render
    credentials_info = json.loads(service_account_json)

    credentials = Credentials.from_service_account_info(
        credentials_info,
        scopes=SCOPES
    )

else:
    # Local Mac
    credentials = Credentials.from_service_account_file(
        "service_account.json",
        scopes=SCOPES
    )

client = gspread.authorize(credentials)

# --------------------------------------------------
# GOOGLE SHEET
# --------------------------------------------------

SPREADSHEET_NAME = "Attended"
WORKSHEET_NAME = "Sheet2"

sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():

    return "Render → Google Sheets connection is working!"


# --------------------------------------------------
# PUSH DATA
# --------------------------------------------------

@app.route("/push", methods=["POST"])
def push_data():

    try:

        data = request.get_json(silent=True)

        if not data:

            return jsonify({
                "success": False,
                "message": "No JSON data received"
            }), 400

        print("Data received:")
        print(data)

        row = [
            data.get("user_id", ""),
            data.get("name", ""),
            data.get("email", ""),
            data.get("phone", ""),
            data.get("service", ""),
            data.get("amount", ""),
            data.get("status", ""),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]

        sheet.append_row(
            row,
            value_input_option="USER_ENTERED"
        )

        print("Data added to Google Sheet:")
        print(row)

        return jsonify({
            "success": True,
            "message": "Data successfully added to Google Sheets",
            "data": row
        }), 200

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------------------------
# TEST ENDPOINT
# --------------------------------------------------

@app.route("/test", methods=["GET"])
def test():

    try:

        test_row = [
            "TEST001",
            "Manual Test",
            "test@gmail.com",
            "9876543210",
            "Test Service",
            "500",
            "Paid",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]

        sheet.append_row(
            test_row,
            value_input_option="USER_ENTERED"
        )

        return jsonify({
            "success": True,
            "message": "Test data added to Google Sheet",
            "data": test_row
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5002))

    app.run(
        host="0.0.0.0",
        port=port
    )
