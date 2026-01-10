# app.py

#CONSIDER USING OPENPYXL

from excel_connector_copy import fullname
from flask import Flask, jsonify
from flask_cors import CORS
from excel_connector_copy import open_wb, save_workbook# Import your existing script

app = Flask(__name__)
CORS(app)  # This allows your React app to talk to this server



@app.route('/open_wb', methods=['POST'])
def open_the_wb():
    try:
        result  = open_wb()
        if result:
            return jsonify({"status": "success", "message": f"{result} has been opened"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/save_wb', methods=['POST'])
def save_wb():
    try:
        result  = save_workbook()
        if result:
            return jsonify({"status": "success", "message": f"{result} has been saved"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

"""
@app.route('/run-excel-task', methods=['POST'])
def run_task():
    try:
        # Call the function from your existing script
        result = your_excel_script.main_logic()
        return jsonify({"status": "success", "message": "Excel file updated!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

"""

if __name__ == '__main__':
    app.run(debug=True, port=5000)
