from flask import Flask, jsonify
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import json

app = Flask(__name__)

# --------------------------------------------------
# GOOGLE SHEETS AUTHENTICATION
# --------------------------------------------------

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

service_account_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")

if not service_account_json:
    raise Exception("GOOGLE_SERVICE_ACCOUNT_JSON environment variable is missing")

credentials_info = json.loads(service_account_json)

credentials = Credentials.from_service_account_info(
    credentials_info,
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

@app.route("/")
def home():
    return "Render → Google Sheets connection is working!"


# --------------------------------------------------
# TEST GOOGLE SHEET
# --------------------------------------------------

@app.route("/test")
def test():

    try:

        test_row = [
            "RENDER001",
            "Render Test",
            "render@test.com",
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
            "message": "Render successfully added data to Google Sheet",
            "data": test_row
        })

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