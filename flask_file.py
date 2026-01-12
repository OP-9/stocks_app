# app.py

#CONSIDER USING OPENPYXL

from flask import Flask, jsonify, request
from flask_cors import CORS
from excel_connector import (open_wb, save_workbook, update_portfolio, 
update_transactions, update_log, update_beta_sheet, stock_names, update_sheets, update_ledger)
import xlwings as xw

app = Flask(__name__)
CORS(app)  # This allows your React app to talk to this server


@app.route('/open_wb', methods=['POST'])
def open_the_wb():
    try:
        result = open_wb()
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

@app.route('/dashboard', methods=['POST'])
def dashboard():
    try:
        if xw.books.active:
            pass
        else:
            open_wb()

        return jsonify({"status": "success", "message": f"Dashboard has been opened"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/update_portfolio', methods=['POST'])
def upd_portfolio():
    try:
        update_portfolio()
        return jsonify({"status": "success", "message": f"Portfolio has been updated"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/transaction', methods=['POST'])
def process_data():
    data = request.get_json()
    date = data.get('date')
    symbol = data.get('symbol')
    action = data.get('action')
    quantity = data.get('quantity')
    price = data.get('price')
    update_transactions(date, symbol, action, quantity, price)
    result = f"Portfolio has been updated with the purchase of {symbol}"
    
    return jsonify({"status": "success", "message": result})

@app.route('/log', methods=['POST'])
def log():
    try:
        result = update_log()
        return jsonify({"status": "success", "message": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/beta_sheet', methods=['POST'])
def beta_sheet():
    try:
        result = update_beta_sheet(stock_names)
        return jsonify({"status":"success", "message":result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/sheets', methods=['POST'])
def upd_sheets():
    try:
        result = update_sheets(stock_names)
        return jsonify({"status":"success", "message":result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/ledger', methods=['POST'])
def upd_ledger():
    try:
        data = request.get_json()
        investor_dict = {}
        time_period = data.get('timePeriod')
        investor_dict['Arun Bhatia'] = float(data.get('arunBhatia'))
        investor_dict['Babita Bhatia'] = float(data.get('babitaBhatia'))
        investor_dict['Aakash Bhatia'] = float(data.get('aakashBhatia'))
        investor_dict['Shikhar Bhatia'] = float(data.get('shikharBhatia'))
        investor_dict['Ajay Bhatia'] = float(data.get('ajayBhatia'))
        result = update_ledger(time_period, investor_dict)
        return jsonify({"status":"success", "message":result}), 200
    except Exception as e:
        return jsonify ({"status":"error", "message":str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
