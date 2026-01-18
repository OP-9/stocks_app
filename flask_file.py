from flask import Flask, jsonify, request
from flask_cors import CORS

from excel_connector import (open_wb, save_workbook, update_portfolio, 
update_transactions, update_log, update_beta_sheet, retrieve_last_update,
stock_names, update_sheets, update_ledger)
from dash_file import create_dash_app

fullname = r'/Users/oneshpunchinilame/Desktop/Programming/stocks_react_app/Portfolio.xlsx'



app = Flask(__name__)
CORS(app)  

create_dash_app(app)

@app.route('/last_update', methods=['GET'])
def update_time():
    try:
        (date_and_time, portfolio_value, invested_amount,
        portfolio_return, portfolio_return_perc) = retrieve_last_update()

        return jsonify({"status": "success", 
        "date_and_time": date_and_time,
        "portfolio_value":portfolio_value, 
        "invested_amount": invested_amount,
        "portfolio_return":portfolio_return,
        "portfolio_return_perc":portfolio_return_perc}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/open_wb', methods=['POST'])
def open_the_wb():
    try:
        result = open_wb(fullname)
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


@app.route('/update_portfolio', methods=['PUT'])
def upd_portfolio():
    try:
        update_portfolio()
        return jsonify({"status": "success", "message": f"Portfolio has been updated"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/transaction', methods=['POST'])
def process_data():
    try:
        data = request.get_json()
        date = data.get('date')
        symbol = data.get('symbol').strip()
        action = data.get('action').strip()
        quantity = float(data.get('quantity'))
        price = float(data.get('price'))

        update_transactions(date, symbol, action, quantity, price)

        return jsonify({"status": "success", "message": f"Portfolio has been updated \
        with the purchase of {symbol}"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


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


@app.route('/sheets', methods=['PUT'])
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

