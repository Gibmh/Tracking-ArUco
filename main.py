from flask import Flask, request, jsonify, render_template
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# --- CONNECT TO GOOGLE SHEET ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open("DB_UAVCUP").sheet1  # tên sheet của bạn


# --- API: GET toàn bộ trạng thái ---
@app.route("/status", methods=["GET"])
def get_status():
    records = sheet.get_all_records()
    return jsonify(records)

@app.route("/update_status", methods=["POST"])
def update_status():
    data = request.json
    num = data.get("Num_Aruco")

    if not num or not (1 <= num <= 16):
        return jsonify({"error": "Num_Aruco phải từ 1 đến 16"}), 400

    rows = sheet.get_all_values()  # bao gồm header
    for i in range(1, len(rows)):
        if rows[i][0] == str(num):
            # Sửa ở đây: phải là list 2 chiều
            sheet.update(f"B{i+1}", [["True"]])
            return jsonify({"message": f"Num_Aruco {num} set to True"})

    return jsonify({"error": "Num_Aruco không tồn tại"}), 404

@app.route("/reset_db", methods=["GET"])
def reset_db():
    rows = sheet.get_all_values()
    for i in range(1,len(rows)):
        sheet.update(f"B{i+1}",[["False"]])

    return jsonify({"message":"Done reset DB for new battle!", "status":True})

@app.route("/")
def index():
    return render_template("index.html")


# --- RUN SERVER ---
if __name__ == "__main__":
    app.run(debug=True)
