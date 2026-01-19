import xlwings as xw
import pandas as pd
import yfinance as yf
import datetime

from dotenv import load_dotenv 
import os 
load_dotenv()


#ENTER PATH OF THE EXCEL WORKBOOK BELOW
fullname = os.getenv("PATH_NAME") 
xw.Book(fullname) 

wb_name = os.getenv("WB_NAME")


stock_names = "" #Initialization of the variable for flask_file to proceed without errors

def open_wb(fullname):
    xw.Book(fullname) 
    workbook_active_name  = active_book_check()
    return workbook_active_name

def active_book_check():
    return xw.books.active.name

def save_workbook():
    workbook_active_name  = active_book_check()
    xw.books[wb_name].save()
    xw.books[wb_name].close()
    
    return workbook_active_name


def add_data_to_portfolio(stock_tickers, money_invested_sum):
    new_portfolio = xw.books[wb_name]
    
    sheet1 = new_portfolio.sheets['Portfolio']

    (current_price, change, two_hundred_day_average, market_cap, fifty_two_week_high, fifty_two_week_low,
     investment_value, today_profit_loss, today_profit_loss_perc, total_profit_loss,
     total_profit_loss_perc) = [[] for _ in range(11)]

    portfolio_sum = float(new_portfolio.sheets['Funds_Portfolio']['A7'].value)

    print("\n Retrieving information from Yahoo Finance...")
    i = 0
    for name in stock_names:
        temp_stock = yf.Ticker(name)
        current_price.append(temp_stock.get_info()['regularMarketPrice'])

        change.append(temp_stock.get_info()['regularMarketChange'])  #regularMarketChange

        two_hundred_day_average.append(temp_stock.get_info()['twoHundredDayAverage'])  #twoHundredDayAverage

        investment_value.append(temp_stock.get_info()['regularMarketPrice'] * quantity_list[i])

        today_profit_loss.append(change[-1] * quantity_list[i])

        today_profit_loss_perc.append(current_price[-1]/(current_price[-1] - change[-1]) -1)

        total_profit_loss.append(investment_value[-1] - money_invested[i])

        total_profit_loss_perc.append(total_profit_loss[-1] / money_invested[i])

        fifty_two_week_high.append(temp_stock.get_info()['fiftyTwoWeekHigh'])

        fifty_two_week_low.append(temp_stock.get_info()['fiftyTwoWeekLow'])

        i += 1

    sheet1['C3'].options(transpose=True).value = stock_names

    sheet1['D3'].options(transpose=True).value = start_dates

    sheet1['E3'].options(transpose=True).value = change

    sheet1['F3'].options(transpose=True).value = current_price

    sheet1['G3'].options(transpose=True).value = quantity_list

    sheet1['H3'].options(transpose=True).value = two_hundred_day_average

    sheet1['I3'].options(transpose=True).value = money_invested

    sheet1['J3'].options(transpose=True).value = investment_value

    sheet1['L3'].options(transpose=True).value = today_profit_loss

    sheet1['M3'].options(transpose=True).value = today_profit_loss_perc

    sheet1['N3'].options(transpose=True).value = total_profit_loss

    sheet1['O3'].options(transpose=True).value = total_profit_loss_perc

    sheet1['P3'].options(transpose=True).value = fifty_two_week_high

    sheet1['Q3'].options(transpose=True).value = fifty_two_week_low

    sheet1['R3'].options(transpose=True).value = sector

    sheet1['S3'].options(transpose=True).value = risk

    date_and_time = datetime.datetime.now()

    #Last Update
    new_portfolio.sheets['Portfolio']['A2'].value = date_and_time.strftime('%d/%m/%Y %I:%M %p')

    #Portfolio Sum
    portfolio_sum += sum(investment_value)
    new_portfolio.sheets['Portfolio']['A4'].value = portfolio_sum

    money_invested_sum = float(new_portfolio.sheets['Funds_Portfolio']['A4'].value)
    money_invested_sum += sum(money_invested)
    new_portfolio.sheets['Portfolio']['A7'].value = money_invested_sum

    #Total Stocks:
    total_stocks = float(new_portfolio.sheets['Funds_Portfolio']['A13'].value)
    total_stocks += sum(quantity_list)
    new_portfolio.sheets['Portfolio']['A9'].value = "Total Stocks"
    new_portfolio.sheets['Portfolio']['A10'].value = total_stocks

    #Returns
    total_profit = float(new_portfolio.sheets['Funds_Portfolio']['A10'].value)
    total_profit += sum(total_profit_loss)
    new_portfolio.sheets['Portfolio']['A14'].value = total_profit

    #Number of Months
    last_row = new_portfolio.sheets['Ledger'].range('A1048576').end('up').row
    num_of_months = last_row - 4 #First entry of month is in cell A5 of Ledger (inclusive of the first month)
    new_portfolio.sheets['Portfolio']['A19'].value = num_of_months #Updates Portfolio page

    #Allocation
    last_row_portfolio = new_portfolio.sheets['Portfolio'].range('C1048576').end('up').row
    sheet1.range('K3:K' + str(last_row_portfolio)).options(transpose=True).formula = '=J3/A$4'
    sheet1.range('K:K').options(transpose=True).number_format = "0.00%"

    #NAV
    sheet1['A24'].value = "NAV"
    sheet1['A25'].formula = '=A4/A10'

    #more_portfolio_calculations(investment_value, portfolio_sum)
    new_portfolio.sheets['Portfolio'].autofit()


def beta_calculator():
    start_dates = []
    last_row = new_portfolio.sheets['Portfolio'].range('D1048576').end('up').row
    for i in range(3, last_row):
        start_dates.append(new_portfolio.sheets['Portfolio']['D' + str(i)].value)
        i += 1
    last_cell_row = new_portfolio.sheets['Beta']['K7'].end('down').row
    last_cell_column = new_portfolio.sheets['Beta']['K7'].end('right').column
    beta_df = new_portfolio.sheets['Beta'].range((7, 8), (last_cell_row, last_cell_column)).options(pd.DataFrame,
                                                                                                    header=1,
                                                                                                    index=False).value



def create_book():
    book_name = input('Enter the name of the workbook: ')
    new_portfolio = xw.Book()
    new_portfolio.save(book_name + '.xlsx')
    new_portfolio.sheets.add('Funds_Portfolio')
    new_portfolio.sheets.add('Beta')
    new_portfolio.sheets.add('Ledger')
    new_portfolio.sheets.add('Transaction History')
    new_portfolio.sheets.add('Log')
    new_portfolio.sheets.add('Portfolio')
    #Adding Elements to Portfolio
    headings = ['Symbol', 'Start Date', 'Change', 'Current Price', 'Amount', '200 Hundred Day Average',
                'Money Invested', 'Investment Value', 'Allocation', 'Today Profit and Loss',
                'Today Profit and Loss (Percentage)', 'Total Profit and Loss', 'Total Profit and Loss (Percentage)',
                '52 Week High', '52 Week Low', 'Sector', 'Risk']
    new_portfolio.sheets['Portfolio']['C2'].value = headings
    new_portfolio.sheets['Portfolio'].range("M:M").number_format = "0.00%"
    new_portfolio.sheets['Portfolio'].range("O:O").number_format = "0.00%"
    new_portfolio.sheets['Portfolio']['A1'].value = "Last Update:"
    new_portfolio.sheets['Portfolio']['A6'].value = "Total Money Invested"

    #Portfolio Value
    new_portfolio.sheets['Portfolio']['A3'].value = "Portfolio Value"

    #Returns
    new_portfolio.sheets['Portfolio']['A12'].value = "Returns"
    new_portfolio.sheets['Portfolio']['A13'].formula = '=A4/A7 -1'
    new_portfolio.sheets['Portfolio']['A13'].number_format = "0.00%"
    new_portfolio.sheets['Portfolio']['A14'].formula = '=A4/A7 -1'

    new_portfolio.sheets['Portfolio']['A16'].value = 'Portfolio Start Date'

    new_portfolio.sheets['Portfolio']['A18'].value = 'No. of Months'

    #Annualized Returns
    new_portfolio.sheets['Portfolio']['A22'].value = "Annualised Returns"
    new_portfolio.sheets['Portfolio']['A23'].formula = '=(A4/A7)^(12/A19)-1'
    new_portfolio.sheets['Portfolio']['A23'].number_format = "0.00%"

    new_portfolio.sheets['Portfolio'].autofit()

    #Log

    log_headings = ['Date', 'Portfolio Value', 'NIFTY 50', 'NAV', 'Portfolio Return', 'Nifty Return', 'NAV Change']
    new_portfolio.sheets['Log']['C4'].value = log_headings
    new_portfolio.sheets['Log'].autofit()

    #Adding Elements to Funds_Portfolio
    new_portfolio.sheets['Funds_Portfolio']['C3'].value = headings

    new_portfolio.sheets['Funds_Portfolio']['A3'].value = 'Total Money Invested In Funds Portfolio'
    money_invested_sum_funds_portfolio = new_portfolio.sheets['Funds_Portfolio'].range('I4:I15')  #Only goes to I15
    new_portfolio.sheets['Funds_Portfolio']['A4'].formula = f'=SUM({money_invested_sum_funds_portfolio.address})'

    new_portfolio.sheets['Funds_Portfolio']['A6'].value = 'Investment Value in Funds_Portfolio'
    investment_sum_funds_portfolio = new_portfolio.sheets['Funds_Portfolio'].range('J4:J15')  #Only goes to J15
    new_portfolio.sheets['Funds_Portfolio']['A7'].formula = f'=SUM({investment_sum_funds_portfolio.address})'

    new_portfolio.sheets['Funds_Portfolio']['A9'].value = 'Total Profit/Loss in Funds_Portfolio'
    total_profit_funds_portfolio = new_portfolio.sheets['Funds_Portfolio'].range('N4:N15')  #Only goes to N15
    new_portfolio.sheets['Funds_Portfolio']['A10'].formula = f'=SUM({total_profit_funds_portfolio.address})'

    new_portfolio.sheets['Funds_Portfolio']['A12'].value = 'Total Stocks'
    total_stocks_funds_portfolio = new_portfolio.sheets['Funds_Portfolio'].range('G4:G15')  #Only goes to G15
    new_portfolio.sheets['Funds_Portfolio']['A13'].formula = f'=SUM({total_stocks_funds_portfolio.address})'

    new_portfolio.sheets['Funds_Portfolio']['A15'].value = 'Low Risk Investment Sum'
    new_portfolio.sheets['Funds_Portfolio']['A18'].value = 'High Risk Investment Sum'

    new_portfolio.sheets['Funds_Portfolio'].autofit()

    #Ledger
    sheet_ledger = new_portfolio.sheets['Ledger']
    ledger_headings = ['Investor', 'Amount Committed', 'Extra Payment', 'Amount Invested', '% Total Fund',
                       'Promised Amount', 'Investment Value', 'Profit/Loss']
    sheet_ledger['I4'].value = ledger_headings
    investors = ['Arun Bhatia', 'Babita Bhatia', 'Aakash Bhatia', 'Shikhar Bhatia', 'Ajay Bhatia']
    sheet_ledger['B4'].value = investors
    sheet_ledger['A4'].value = 'Month'

    sheet_ledger['I5'].options(transpose=True).value = investors
    sheet_ledger['I11'].value = 'Totals'
    sheet_ledger['J11'].formula = '=J5 + J6 + J7 + J8 + J9'
    sheet_ledger['L11'].formula = '=L5 + L6 + L7 + L8 + L9'
    sheet_ledger.range('M5:M9').formula = '=L5/L$11'
    sheet_ledger.range('M:M').number_format = '0.00%'
    sheet_ledger['N11'].formula = '=L11 * 1.14'
    sheet_ledger['O11'].formula = '=O5 + O6 + O7 + O8 + O9'
    sheet_ledger['P11'].formula ='=O11/L11-1'
    sheet_ledger['P11'].number_format = '0.00%'

    new_portfolio.sheets['Ledger'].autofit()

    #Transaction History
    headings_transaction_hist = ['Date', 'Symbol', 'Action', 'Quantity', 'Price', 'Amount']
    new_portfolio.sheets['Transaction History']['E4'].value = headings_transaction_hist

    new_portfolio.sheets['Transaction History'].autofit()
    return new_portfolio


def create_stock_sheets(stock_names):
    new_portfolio = xw.books[wb_name]

    print('\nCreating Sheets...\n')
    stocks_download = yf.download(stock_tickers, start=portfolio_start_date)
    stocks_download = stocks_download['Close']
    stocks_download.reset_index(inplace=True)
    #stocks_download = stocks_download.reindex(columns= stock_names)
    headings = ['Date', 'Closing Price', 'Change %']

    i = 0
    for symbol in stock_names:
        new_portfolio.sheets.add(symbol, after='Funds_Portfolio')
        new_portfolio.sheets[symbol]['D3'].value = 'Name'
        new_portfolio.sheets[symbol]['E3'].value = symbol
        new_portfolio.sheets[symbol]['D4'].value = 'First Purchased on'
        new_portfolio.sheets[symbol]['E4'].value = start_dates[i]
        new_portfolio.sheets[symbol]['D5'].value = 'Risk'
        new_portfolio.sheets[symbol]['E5'].value = risk[-1]
        new_portfolio.sheets[symbol]['H3'].value = headings
        new_portfolio.sheets[symbol]['H4'].options(transpose=True).value = list(stocks_download['Date'])
        new_portfolio.sheets[symbol]['I4'].options(transpose=True).value = list(stocks_download[symbol])
        new_portfolio.sheets[symbol].range("J5:J500").formula = "=I5/I4 - 1"
        new_portfolio.sheets[symbol].range("J:J").number_format = "0.00%"
        i += 1
        new_portfolio.sheets[symbol].autofit()

    print('\nDone!\n')


def excel_reader():
    new_portfolio = xw.books[wb_name]

    #Identifying the last used cell in sheet Portfolio, indicates end of table
    last_row = new_portfolio.sheets['Portfolio'].range('C1048576').end('up').row
    portfolio_df = new_portfolio.sheets['Portfolio'].range('C2:S' + str(last_row)).options(pd.DataFrame, header=1,
                                                                                           index=False).value

    money_invested_sum = float(new_portfolio.sheets['Portfolio']['A7'].value)
    portfolio_start_date = new_portfolio.sheets['Portfolio']['A17'].value
    stocks_dict = {}

    for i in range(len(portfolio_df['Symbol'])):
        stocks_dict[portfolio_df['Symbol'][i]] = [float(portfolio_df['Amount'][i]),
                                                  float(portfolio_df['Money Invested'][i])]

    stock_names = list(portfolio_df['Symbol'])
    quantity_list = list(portfolio_df['Amount'])
    money_invested = list(portfolio_df['Money Invested'])
    start_dates = list(portfolio_df['Start Date'])
    sector = list(portfolio_df['Sector'])
    risk = list(portfolio_df['Risk'])
    stock_tickers = ', '.join(stock_names)

    return stocks_dict, stock_tickers, stock_names, quantity_list, money_invested, money_invested_sum, start_dates, sector, risk, portfolio_start_date, portfolio_df


#Add a minimum of two initial stocks
def initial_stock_tickers():
    new_portfolio = xw.books[wb_name]

    stocks_dict = {}
    start_dates, quantity_list, money_invested, risk, sector = [[] for i in range(5)]
    portfolio_start_date = input('Enter the date on which this portfolio was \
        started in DD/MM/YYYY: ')
    new_portfolio.sheets['Portfolio']['A17'].value = portfolio_start_date
    print("Enter the intial ticker symbols in one sentence below, seperating each \
    symbol with a comma, like so: AAPL, GOOGL ")
    stock_tickers = input("Enter the ticker symbols: ")
    stock_names = stock_tickers.split(', ')
    new_portfolio.sheets['Transaction History']['N5'].value = stock_names
    headings = ['Symbol', 'Start Date', 'Change', 'Current Price', 'Amount', 
                '200 Hundred Day Average', 'Money Invested', 'Investment Value', 
                'Allocation', 'Today Profit and Loss', 'Today Profit and Loss (Percentage)', 
                'Total Profit and Loss', 'Total Profit and Loss (Percentage)',
                '52 Week High', '52 Week Low', 'Sector']

    money_invested_sum = new_portfolio.sheets['Funds_Portfolio']['A4'].value
    print("\nDo not use commas or symbols when entering either the money invested \
        or quantity purchased.\n")

    for name in stock_names:
        print(f"\n{name}\n")
        quantity = int(input('Enter the quantity: '))
        money_invested_input = float(input(f"\nEnter the money invested in {name}: "))
        start_dates.append(input(f"\nEnter the date on which {name} was first \
            purchased in DD/MM/YYYY form: "))
        sector.append(input(f"\nEnter the sector of {name}: "))
        risk.append(input(f"\nEnter the risk of {name} (HIGH/LOW): "))
        money_invested.append(money_invested_input)
        stocks_dict[name] = [quantity, money_invested_input]
        quantity_list.append(quantity)
        money_invested_sum += money_invested_input

    new_portfolio.sheets['Transaction History']['N6'].value = quantity_list
    new_portfolio.sheets['Transaction History'].autofit()
    new_portfolio.sheets['Portfolio']['A7'].value = money_invested_sum

    return stock_tickers, stocks_dict, quantity_list, stock_names, money_invested, money_invested_sum, start_dates, sector, risk


def retrieve_stock_data(stock_tickers):
    stock_data = yf.Tickers(stock_tickers)
    return stock_data

def retrieve_last_update():
    new_portfolio = xw.books[wb_name]

    date_and_time = new_portfolio.sheets['Portfolio']['A2'].value
    #date_and_time = date_and_time.replace(" ", ", ")
    date_and_time = date_and_time.strftime('%d/%m/%Y, %I:%M %p')

    portfolio_value = float(new_portfolio.sheets['Portfolio']['A4'].value)
    portfolio_value = f"₹ {portfolio_value:,.2f}"

    invested_amount = float(new_portfolio.sheets['Portfolio']['A7'].value)
    invested_amount = f"₹ {invested_amount:,.2f}"

    portfolio_return = float(new_portfolio.sheets['Portfolio']['A14'].value)
    portfolio_return = f"₹ {portfolio_return:,.2f}"

    portfolio_return_perc = float(new_portfolio.sheets['Portfolio']['A13'].value)
    portfolio_return_perc = f"{portfolio_return_perc:.2%}"

    
    return date_and_time, portfolio_value, invested_amount, portfolio_return, portfolio_return_perc


def risk_table():
    new_portfolio = xw.books[wb_name]

    sheet_ledger = new_portfolio.sheets['Ledger']
    sheet_ledger['R5'].value = 'Portfolio Value'
    sheet_ledger['S5'].value = new_portfolio.sheets['Portfolio']['A4'].value

    sheet_ledger['R4'].value = 'Ideal Minimum Value'
    sheet_ledger['S4'].value = sheet_ledger['L11'].value

    headings = ['Risk', 'Allocation %', 'Allocation Value', 'Current %', 'Current Value', 'To reduce/add']
    sheet_ledger['R6'].value = headings
    sheet_ledger['R7'].value = ['Low Risk', 0.5]
    sheet_ledger['R8'].value = ['High Risk', 0.5]

    sheet_ledger.range('S7:S8').number_format = "0.00%"

    portfolio_df['Risk'] = portfolio_df['Risk'].astype(str)

    low_risk_stocks = portfolio_df[portfolio_df['Risk'] == "LOW"]
    high_risk_stocks = portfolio_df[portfolio_df['Risk'] == "HIGH"]
    low_risk_stocks_sum = float(new_portfolio.sheets['Funds_Portfolio']['A16'].value)
    high_risk_stocks_sum = float(new_portfolio.sheets['Funds_Portfolio']['A19'].value)

    low_risk_stocks_sum += low_risk_stocks['Investment Value'].sum()
    high_risk_stocks_sum += high_risk_stocks['Investment Value'].sum()

    sheet_ledger['V7'].value = low_risk_stocks_sum
    sheet_ledger['V8'].value = high_risk_stocks_sum

    sheet_ledger['U7'].formula = '=V7/S5'
    sheet_ledger['U8'].formula = '=V8/S5'

    sheet_ledger.range('U:U').number_format = '0.00%'

    sheet_ledger['T7'].formula = '=S7*S4'
    sheet_ledger['T8'].formula = '=S8*S4'

    sheet_ledger['W7'].formula = '=T7-V7'
    sheet_ledger['W8'].formula = '=T8-V8'

    sheet_ledger.autofit()


def update_beta_sheet(stock_names):
    new_portfolio = xw.books[wb_name]

    print("\nUpdating Beta Sheet...")
    portfolio_weight = list(portfolio_df['Allocation'])
    new_portfolio.sheets['Beta']['K3'].value = stock_names
    new_portfolio.sheets['Beta']['K5'].value = portfolio_weight
    last_row_beta_sheet = new_portfolio.sheets['Beta'].range('J1048576').end('up').row
    last_update = new_portfolio.sheets['Beta']['J8'].value  
    stocks_history_download = yf.download('^NSEI', start=last_update)
    stocks_history_download = stocks_history_download['Close']
    stocks_history_download = stocks_history_download.reset_index()
    prices = stocks_history_download['^NSEI'].to_list()

    new_portfolio.sheets['Beta']['F8'].options(transpose=True).value = list(stocks_history_download['Date'])

    new_portfolio.sheets['Beta']['J5'].value = 'Portfolio Weight'
    new_portfolio.sheets['Beta']['F7'].value = 'Date'
    new_portfolio.sheets['Beta']['G7'].value = 'NIFTY 50'
    new_portfolio.sheets['Beta']['G8'].options(transpose=True).value = prices

    new_portfolio.sheets['Beta']['I7'].value = 'Portfolio Returns'

    new_portfolio.sheets['Beta']['H7'].value = 'NIFTY Returns'
    new_portfolio.sheets['Beta'].range("H9:H1048576").formula = "=G9/G8 - 1"
    new_portfolio.sheets['Beta'].range("H:H").number_format = "0.00%"

    update_sheets(stock_names)

    last_row_stock_sheets = new_portfolio.sheets[stock_names[0]].range('H1048576').end('up').row

    i = 11
    for name in stock_names:
        temp_df = new_portfolio.sheets[name].range('H3:J' + str(last_row_stock_sheets + 1)).options(pd.DataFrame,
                                                                                                    header=1,
                                                                                                    index=False).value
        # NIFTY50 is missing data from 5th Nov
        # Solution: merge dataframes on NIFTY50 dates
        temp_df_merged = stocks_history_download.merge(temp_df, left_on='Date', right_on='Date', how='left')
        new_portfolio.sheets['Beta'].range((7, i)).value = name
        new_portfolio.sheets['Beta'].range((8, i)).options(transpose=True).value = list(temp_df_merged['Change %'])
        i += 1

    new_portfolio.sheets['Beta']['J6'].value = 'Beta'
    new_portfolio.sheets['Beta']['J7'].value = 'Date'
    new_portfolio.sheets['Beta']['J8'].options(transpose=True).value = list(temp_df_merged['Date'])
    new_portfolio.sheets['Beta'].autofit()
    return "Done updating Beta sheet!\n"


def update_ledger(time_period, investor_dict):
    new_portfolio = xw.books[wb_name]

    ledger_df = new_portfolio.sheets['Ledger'].range('I4:P9').options(pd.DataFrame, header=1, index=False).value

    ledger_df['Amount Invested'] = ledger_df['Amount Invested'].astype(float)

    ledger_dict = dict(zip(ledger_df['Investor'], ledger_df['Amount Invested']))
    money_added_list = list(ledger_df['Amount Invested'])
    last_row = new_portfolio.sheets['Ledger'].range('A1048576').end('up').row
    
    i = 0
    for investor in ledger_df['Investor']:
        money_added = investor_dict[investor]
        if money_added > 0:
            new_portfolio.sheets['Ledger'].range((last_row + 1, i + 2)).value = "Paid"
        else:
            new_portfolio.sheets['Ledger'].range((last_row + 1, i + 2)).value = "Unpaid"
        money_added_list[i] = money_added_list[i] + money_added
        ledger_dict[investor] = ledger_dict[investor] + money_added
        i += 1

    new_portfolio.sheets['Ledger']['L5'].options(transpose=True).value = money_added_list

    new_cell = new_portfolio.sheets['Ledger']['A' + str(last_row + 1)]
    new_cell.value = time_period

    return 'Ledger updated!'


def update_log():
    new_portfolio = xw.books[wb_name]
    last_row = new_portfolio.sheets['Log'].range('C1048576').end('up').row
    prev_date = new_portfolio.sheets['Log']['C' + str(last_row)].value
    print(f"\nThe log was last updated on: {prev_date}\n")
    new_row = last_row + 1
    portfolio_value = float(new_portfolio.sheets['Portfolio']['A4'].value)
    prev_portfolio_value = float(new_portfolio.sheets['Log']['D' + str(last_row)].value)
    date_and_time = datetime.datetime.now()
    date_and_time.strftime('%d/%m/%Y')

    new_portfolio.sheets['Log']['C' + str(new_row)].value = date_and_time
    new_portfolio.sheets['Log']['D' + str(new_row)].value = portfolio_value
    new_portfolio.sheets['Log']['E' + str(new_row)].value = yf.Ticker('^NSEI').get_info()['regularMarketPrice']
    new_portfolio.sheets['Log']['F' + str(new_row)].value = float(new_portfolio.sheets['Portfolio']['A25'].value)
    new_portfolio.sheets['Log']['G' + str(new_row)].value = portfolio_value / prev_portfolio_value - 1
    new_portfolio.sheets['Log']['H' + str(new_row)].value = float(new_portfolio.sheets['Log']['E' + str(new_row)].value) / \
                                                            float(new_portfolio.sheets['Log']['E' + str(last_row)].value) - 1
    new_portfolio.sheets['Log']['I' + str(new_row)].value = float(new_portfolio.sheets['Log']['F' + str(new_row)].value) / \
                                                            float(new_portfolio.sheets['Log']['F' + str(last_row)].value) - 1

    return f"\nThe log was last updated on: {prev_date}.\n Log has been updated!\n"


def update_portfolio():
    new_portfolio = xw.books[wb_name]
    print("\nStarting Portfolio Update\n")
    new_portfolio = xw.books[active_book_check()]
    money_invested_sum = float(new_portfolio.sheets['Funds_Portfolio']['A4'].value)
    stock_tickers = ', '.join(stock_names)
    new_portfolio.sheets['Portfolio']['A12'].value = "Returns"
    new_portfolio.sheets['Portfolio']['A13'].formula = '=A4/A7 -1'
    new_portfolio.sheets['Portfolio']['A13'].number_format = "0.00%"
    new_portfolio.sheets['Portfolio']['A14'].formula = '=A4/A7 -1'

    add_data_to_portfolio(stock_tickers, money_invested_sum)

    print("Update completed :)")


def update_portfolio_dashboard(stock_names, quantity_list):
    new_portfolio = xw.books[wb_name]
    current_price, investment_value, total_profit_loss = [[] for i in range(3)]
    portfolio_sum = float(new_portfolio.sheets['Funds_Portfolio']['A7'].value)
    total_profit = float(new_portfolio.sheets['Funds_Portfolio']['A10'].value)
    i = 0
    for name in stock_names:
        temp_stock = yf.Ticker(name)
        temp_price = temp_stock.get_info()['regularMarketPrice']
        current_price.append(temp_price)
        investment_value.append(temp_price * quantity_list[i])
        total_profit_loss.append(investment_value[-1] - money_invested[i])
        i += 1
    portfolio_sum += sum(investment_value)
    total_profit += sum(total_profit_loss)
    new_portfolio.sheets['Portfolio']['A14'].value = total_profit
    new_portfolio.sheets['Portfolio']['A4'].value = portfolio_sum
    return portfolio_sum


def update_sheets(stock_names):
    new_portfolio = xw.books[wb_name]
    print('\nUpdating Sheets...\n')
    for name in stock_names:
        last_row = new_portfolio.sheets[name].range('H1048576').end('up').row
        last_update = new_portfolio.sheets[name]['H' + str(last_row)].value
        if datetime.datetime.now().strftime("%Y-%m-%d") != last_update:
            last_update = str(last_update.strftime("%Y-%m-%d"))
            stocks_history_download = yf.download(name, start=last_update)
            stocks_history_download = stocks_history_download['Close']
            stocks_history_download = stocks_history_download.reset_index()
            dates = list(stocks_history_download['Date'][1:])
            prices = list(stocks_history_download[name][1:])
            new_portfolio.sheets[name]['H' + str(last_row + 1)].options(transpose=True).value = dates
            new_portfolio.sheets[name]['I' + str(last_row + 1)].options(transpose=True).value = prices
            new_portfolio.sheets[name].range("I:I").number_format = "0.00"
            new_portfolio.sheets[name].range("J5:J500").formula = "=I5/I4 - 1"
            new_portfolio.sheets[name].range("J:J").number_format = "0.00%"

    return "Done updating sheets!"


def update_transactions(date, symbol, action, quantity, price):  #Function to add new entries to new_portfolio[Transaction History]
    new_portfolio = xw.books[wb_name]

    money_invested_sum = float(new_portfolio.sheets['Portfolio']['A7'].value)

    print('\nAdding purchase of stock(s)...')
    
    if action == 'SELL':
        quantity = -1 * float(quantity)

    amount = float(quantity) * float(price)

    right_most_value = new_portfolio.sheets['Transaction History'].range('N5').end('right').column
    money_invested_sum += amount

    if symbol not in stocks_dict:
        sector.append(input(f"\nEnter the sector of {symbol}: "))
        risk.append(input(f"\nEnter the risk of {symbol} (HIGH/LOW): "))
        money_invested.append(amount)
        stocks_dict[symbol] = [quantity, amount]
        stock_names.append(symbol)
        quantity_list.append(quantity)
        start_dates.append(date)
        symbol_list = [symbol]

        headings = ['Date', 'Closing Price', 'Change %']
        # Creating the Symbol's sheet
        stocks_download = yf.download(symbol, start= portfolio_start_date)
        stocks_download = stocks_download['Close']
        stocks_download.reset_index(inplace=True)
        new_portfolio.sheets.add(symbol, after='Funds_Portfolio')
        new_portfolio.sheets[symbol]['D3'].value = 'Name'
        new_portfolio.sheets[symbol]['E3'].value = symbol
        new_portfolio.sheets[symbol]['D4'].value = 'First Purchased on'
        new_portfolio.sheets[symbol]['E4'].value = date
        new_portfolio.sheets[symbol]['D5'].value = 'Risk'
        new_portfolio.sheets[symbol]['E5'].value = risk[-1]
        new_portfolio.sheets[symbol]['H3'].value = headings
        new_portfolio.sheets[symbol]['H4'].options(transpose=True).value = list(stocks_download['Date'])
        new_portfolio.sheets[symbol]['I4'].options(transpose=True).value = list(stocks_download[symbol])
        new_portfolio.sheets[symbol].range("J5:J500").formula = "=I5/I4 - 1"
        new_portfolio.sheets[symbol].range("J:J").number_format = "0.00%"

        new_portfolio.sheets['Transaction History'].range((5, right_most_value + 1)).value = symbol
        new_portfolio.sheets['Transaction History'].range((6, right_most_value + 1)).value = quantity
        new_portfolio.sheets[symbol].autofit()

    else:
        temp_quantity = stocks_dict[symbol][0]
        temp_quantity = int(temp_quantity) + int(quantity)

        temp_money_invested = stocks_dict[symbol][1]
        temp_money_invested = float(temp_money_invested) + float(amount)

        stocks_dict[symbol] = [temp_quantity, temp_money_invested]


    last_row = new_portfolio.sheets['Transaction History'].range('E1048576').end('up').row
    new_row = 1 + last_row

    new_portfolio.sheets['Transaction History']['E' + str(new_row)].value = date
    new_portfolio.sheets['Transaction History']['F' + str(new_row)].value = symbol
    new_portfolio.sheets['Transaction History']['G' + str(new_row)].value = action
    new_portfolio.sheets['Transaction History']['H' + str(new_row)].value = quantity
    new_portfolio.sheets['Transaction History']['I' + str(new_row)].value = price
    new_portfolio.sheets['Transaction History']['J' + str(new_row)].value = amount

    new_portfolio.sheets['Portfolio']['A7'].value = money_invested_sum

    new_portfolio.sheets['Transaction History']['N5'].value = stock_names
    for i in range(len(stock_names)):
        quantity_list[i] = stocks_dict[stock_names[i]][0]
        money_invested[i] = stocks_dict[stock_names[i]][1]
    new_portfolio.sheets['Transaction History']['N6'].value = quantity_list


    new_portfolio.sheets['Transaction History'].autofit()

    update_portfolio()


#LEAVE THE ITEMS BELOW UNCOMMENTED

new_portfolio = xw.books[wb_name]
(stocks_dict, stock_tickers, stock_names, quantity_list, money_invested, money_invested_sum,
start_dates, sector, risk, portfolio_start_date, portfolio_df) = excel_reader()


