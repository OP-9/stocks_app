from flask import Flask, jsonify, request
from flask_cors import CORS

from excel_connector import (fullname, open_wb, save_workbook, update_portfolio, 
update_transactions, update_log, update_beta_sheet, retrieve_last_update,
stock_names, update_sheets, update_ledger, risk_table)




app = Flask(__name__)
CORS(app)  

#CALLING CREATE_DASH_APP FROM DASH_FILE TO LAUNCH THE DASHBOARD
try:
    from dash_file import create_dash_app

    create_dash_app(app)

except:
    "Error, could not import the Dash App. Ensure the workbook's name and location are correct and re-run the Flask app."



#DISPLAYS SELECT INFORMATION AS OF THE LAST UPDATE OF THE PORTFOLIO
@app.route('/last_update', methods=['GET'])
def update_time():
    try:
        (date_and_time, portfolio_value, invested_amount,
        portfolio_return, portfolio_return_perc) = retrieve_last_update()

        return jsonify({"status": "success", 
        "message": "updated",
        "date_and_time": date_and_time,
        "portfolio_value":portfolio_value, 
        "invested_amount": invested_amount,
        "portfolio_return":portfolio_return,
        "portfolio_return_perc":portfolio_return_perc}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#OPENS THE PORTFOLIO EXCEL WORKBOOK
@app.route('/open_wb', methods=['POST'])
def open_the_wb():
    try:
        result = open_wb(fullname)
        if result:
            return jsonify({"status": "success", "message": f"{result} has been opened"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#SAVES AND CLOSES THE WORKBOOK
@app.route('/save_wb', methods=['POST'])
def save_wb():
    try:
        result  = save_workbook()
        if result:
            return jsonify({"status": "success", "message": f"{result} has been saved"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#UPDATES THE PORTFOLIO SHEET
@app.route('/update_portfolio', methods=['PUT'])
def upd_portfolio():
    try:
        update_portfolio()
        risk_table()
        return jsonify({"status": "success", "message": f"Portfolio has been updated"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#ALLOWS USER TO ADD A PURCHASE/SALE OF STOCK(S)
@app.route('/transaction', methods=['POST'])
def process_data():
    try:
        data = request.get_json()
        date = data.get('date')
        symbol = data.get('symbol').strip()
        action = data.get('action').strip()
        quantity = float(data.get('quantity'))
        price = float(data.get('price'))
        sector_input, risk_input = None, None

        if data.get('sector') is not None:
            sector_input = data.get('sector').strip()
            risk_input = data.get('risk').strip()

        update_transactions(date, symbol, action, quantity, price, sector_input, risk_input)

        return jsonify({"status": "success", "message": f"Portfolio has been updated with the purchase of {symbol}"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#UPDATES THE LOG SHEET
@app.route('/log', methods=['POST'])
def log():
    try:
        result = update_log()
        return jsonify({"status": "success", "message": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#UPDATES THE BETA SHEET
@app.route('/beta_sheet', methods=['POST'])
def beta_sheet():
    try:
        result = update_beta_sheet(stock_names)
        return jsonify({"status":"success", "message":result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#UPDATES THE STOCK SHEETS
@app.route('/sheets', methods=['PUT'])
def upd_sheets():
    try:
        result = update_sheets(stock_names)
        return jsonify({"status":"success", "message":result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#UPDATES THE LEDGER
@app.route('/ledger', methods=['POST'])
def upd_ledger():
    try:
        data = request.get_json()
        investor_dict = {}
        time_period = data.get('timePeriod')

        investor_dict['Investor1'] = float(data.get('Investor1'))
        investor_dict['Investor2'] = float(data.get('Investor2'))
        investor_dict['Investor3'] = float(data.get('Investor3'))
        investor_dict['Investor4'] = float(data.get('Investor4'))
        investor_dict['Investor5'] = float(data.get('Investor5'))
        result = update_ledger(time_period, investor_dict)
        return jsonify({"status":"success", "message":result}), 200

    except Exception as e:
        return jsonify ({"status":"error", "message":str(e)}), 500

