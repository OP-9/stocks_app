# app.py

#CONSIDER USING OPENPYXL

from flask import Flask, jsonify
from flask_cors import CORS
import your_excel_script  # Import your existing script

app = Flask(__name__)
CORS(app)  # This allows your React app to talk to this server

@app.route('/run-excel-task', methods=['POST'])
def run_task():
    try:
        # Call the function from your existing script
        result = your_excel_script.main_logic()
        return jsonify({"status": "success", "message": "Excel file updated!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)