import xlwings as xw
from excel_connector import excel_reader, update_log, update_portfolio, update_transactions, update_ledger, risk_table, \
 update_beta_sheet
from dash_file import app

#LEAVE THIS UNCOMMENTED
new_portfolio = xw.books['Portfolio.xlsx']
#LEAVE THIS UNCOMMENTED
(stocks_dict, stock_tickers, stock_names, quantity_list, money_invested, money_invested_sum,
 start_dates, sector, risk, portfolio_start_date, portfolio_df) = excel_reader()

#TO UPDATE PORTFOLIO
update_portfolio()

#AFTER PERFORMING A TRANSACTION
#update_transactions()
#risk_table()
#update_portfolio()

#TO UPDATE LOG
#update_log()

#TO UPDATE BETA SHEET & INDIVIDUAL STOCK SHEETS
#update_beta_sheet(stock_names)

#UPDATING LEDGER
#update_ledger()

#DISPLAY PORTFOLIO ON WEBSITE
if __name__ == '__main__':
 app.run(debug=True)