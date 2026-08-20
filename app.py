from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

# Google Sheets authentication
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_file(
    "service_account.json",
    scopes=SCOPES
)

client = gspread.authorize(credentials)

# Google Sheet
SPREADSHEET_NAME = "Attended"
WORKSHEET_NAME = "Sheet2"

sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)


@app.route("/")
def home():
    return "Google Sheets connection is working!"


@app.route("/test", methods=["GET"])
def test():

    try:

        test_row = [
            "TEST001",
            "Test User",
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
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5002,
        debug=True
    )