from logger_setup import setup_logging
setup_logging()

from flask import Flask, jsonify, request
from flask_cors import CORS
from waitress import serve
import logging

from dash_file import portfolio, create_dash_app
from excel_connector import Portfolio



logger = logging.getLogger('backend')

app = Flask(__name__)
CORS(app)  

#CALLING CREATE_DASH_APP FROM DASH_FILE TO LAUNCH THE DASHBOARD
try:

    create_dash_app(app)

except:
    print("Error, could not import the Dash App. Ensure the workbook's name \
and location are correct and re-run the Flask app.")
    logger.debug("Error", exc_info=True)



#DISPLAYS SELECT INFORMATION AS OF THE LAST UPDATE OF THE PORTFOLIO
@app.route('/last_update', methods=['GET'])
def update_time():
    try:
        (date_and_time, portfolio_value, invested_amount,
        portfolio_return, portfolio_return_perc) = portfolio.retrieve_last_update()

        return jsonify({"status": "success", 
        "message": "updated",
        "date_and_time": date_and_time,
        "portfolio_value":portfolio_value, 
        "invested_amount": invested_amount,
        "portfolio_return":portfolio_return,
        "portfolio_return_perc": portfolio_return_perc}), 200

    except Exception as e:
        logger.debug("Error", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


#SAVES AND CLOSES THE WORKBOOK
@app.route('/save_wb', methods=['POST'])
def save_wb():
    try:
        result  = portfolio.final_safe_save()
        if result:
            return jsonify({"status": "success", "message": f"{result}"}), 200

    except Exception as e:
        logger.debug("Error", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


#UPDATES THE PORTFOLIO SHEET
@app.route('/update_portfolio', methods=['PUT'])
def upd_portfolio():
    try:
        
        logger.debug("App route upd_portfolio")
        portfolio.update_portfolio()
        
        return jsonify({"status": "success", "message": "Portfolio has been updated"}), 200

    except Exception as e:
        logger.debug("Error", exc_info=True)
        return jsonify({
            "status": "error", 
            "message": str(e)}), 500


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

        portfolio.update_transactions_wrapper(date, symbol, action, quantity, price, sector_input, risk_input)

        return jsonify({"status": "success", 
        "message": f"Portfolio has been updated with the purchase of {symbol}"}), 200

    except Exception as e:
        logger.debug("Error", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


#UPDATES THE LOG SHEET
@app.route('/log', methods=['PUT'])
def log():
    try:
        result = portfolio.update_log()
        return jsonify({"status": "success", "message": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#UPDATES THE BETA SHEET
@app.route('/beta_sheet', methods=['POST'])
def beta_sheet():
    try:
        portfolio.update_beta_sheet()
        return jsonify({"status":"success", "message":"Done updating Beta sheet!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#UPDATES THE STOCK SHEETS
@app.route('/sheets', methods=['PUT'])
def upd_sheets():
    try:
        logger.debug("App route upd_sheets")
        portfolio.update_sheets_thread()
        return jsonify({"status":"success", "message":"Done updating sheets!"}), 200
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
        result = portfolio.update_ledger(time_period, investor_dict)
        return jsonify({"status":"success", "message":result}), 200

    except Exception as e:
        return jsonify ({"status":"error", "message":str(e)}), 500


if __name__ == '__main__':
    print("Starting app...\n")
    #app.run(debug=True, host='0.0.0.0', port=5000)
    #print("Server is running on http://localhost:5173")
    
    #Production WSGI server
    serve(app, host='0.0.0.0', port=5000)
    print("Server is running on http://localhost:3000")