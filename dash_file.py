import dash
from dash.dependencies import Output, Input
from dash import dcc, html, dash_table
import plotly.express as px
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import xlwings as xw
import datetime

try:
    from excel_connector import excel_reader, update_portfolio_dashboard, new_portfolio

    start_date = new_portfolio.sheets['Portfolio']['A17'].value
    start_date = start_date.strftime('%Y-%m-%d')

    stocks_dict, stock_tickers, stock_names, quantity_list, money_invested, money_invested_sum, start_dates, sector, risk, portfolio_start_date, portfolio_df = excel_reader()

    allocation_df = portfolio_df[['Symbol', 'Allocation']]
    allocation_df.loc[:,'Allocation'] = allocation_df.loc[:,'Allocation'] * 100

    investor_df_og = new_portfolio.sheets['Ledger'].range('I4:S9').options(pd.DataFrame, header=1, index=False).value
    investor_df = investor_df_og[['Investor', 'Amount Invested', 'Profit/Loss']].copy() #'% Total Fund',
    investor_df['Profit/Loss'] = investor_df['Profit/Loss'].map('{:.2%}'.format)
    investor_df['Amount Invested'] = investor_df['Amount Invested'].map('₹{:,.2f}'.format)


    sector_df = portfolio_df[['Symbol', 'Sector', 'Allocation']]
    sector_df.loc[:,'Allocation'] = sector_df.loc[:,'Allocation'] * 100

    sector_returns_df = portfolio_df[['Symbol', 'Sector', 'Today Profit and Loss (Percentage)', 'Total Profit and Loss (Percentage)']]
    sector_returns_df.loc[:,'Today Profit and Loss (Percentage)'] = 100 * sector_returns_df.loc[:,'Today Profit and Loss (Percentage)']
    sector_returns_df.loc[:,'Total Profit and Loss (Percentage)'] = 100 * sector_returns_df.loc[:,'Total Profit and Loss (Percentage)']

    risk_table_df = new_portfolio.sheets['Ledger'].range('R6:W8').options(pd.DataFrame, header=1, index=False).value
    risk_table_df['Allocation %'] = risk_table_df['Allocation %'].map('{:.2%}'.format)
    risk_table_df['Current %'] = risk_table_df['Current %'].map('{:.2%}'.format)
    risk_table_df['Allocation Value'] = risk_table_df['Allocation Value'].map('₹{:,.2f}'.format)
    risk_table_df['Current Value'] = risk_table_df['Current Value'].map('₹{:,.2f}'.format)
    risk_table_df['To reduce/add'] = risk_table_df['To reduce/add'].map('₹{:,.2f}'.format)

except:
    pass


def create_dash_app(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dashboard/")

    colors = {
        'background': '#f8f9fa',
        'text': 'black',
        'card_background': 'white'
    }

    card_style = {
        'backgroundColor': colors['card_background'],
        'borderRadius': '10px',
        'padding': '20px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'marginBottom': '20px'
    }

    header_style = {
        'backgroundColor': '#2596be',
        'color': 'white',
        'padding': '20px',
        'borderRadius': '10px',
        'marginBottom': '30px'
    }

    # Ticker symbol to track
    TICKER_SYMBOL = '^NSEI'

    nifty = yf.Ticker(TICKER_SYMBOL)
    name = nifty.info['shortName']

    dash_app.layout = html.Div(style={'fontFamily': 'Lato, Roboto, sans-serif', 'backgroundColor': colors['background'], 'margin':'1%'},
    children = [

        html.Div([ #SECTION 1, TITLE
            html.Div([
                html.H1("Stocks Portfolio Dashboard", style={'textAlign':'center'})
                ]),
                html.Div([ #SECTION 1, TIME
                    html.Div(id='time')
                ])
                ],style=header_style),

            html.Div([ #SECTION 2
                    html.Div([  # LIVE DISPLAY OF PORTFOLIO
                    html.H3("Portfolio Value"),
                    html.Div(id='live-update-price_portfolio'),
                        ],style={**card_style, 'textAlign': 'center', 'color': 'black',}),

                    html.Div([  # LIVE DISPLAY OF RETURNS OR MAYBE BEST PERFORMING STOCK ATM
                        html.H3("Total Return"),
                        html.Div(id='returns',),
                        ],style={**card_style, 'textAlign': 'center', 'color': 'black',}
                        ),
                    
                    html.Div([
                        html.H3("Live Price of NIFTY 50"),
                        html.Div(id='live-update-price-nifty') #NIFTY 50 PRICE UPDATE
                        ],style={**card_style, 'textAlign': 'center', 'color': 'black',}),

                    html.Div([
                        html.H3("Current NAV"),
                        html.Div(id='live-update-nav'), #NAV UPDATE
                        ],style={**card_style, 'textAlign': 'center', 'color': 'black',})
                    ],style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '20px',
                    'marginBottom': '30px'}),

            html.Div([ #SECTION 3
                html.Div([  #TITLE OF GRAPHS
                    html.H3("Performance of NAV and NIFTY 50")
                    ],style={'textAlign':'center'}),

                html.Div([  #GRAPH
                    dcc.Dropdown(['NAV', 'NIFTY 50', 'NAV & NIFTY 50'], 'NAV & NIFTY 50', id='dropdown-selection'),
                    dcc.Graph(id='graph-content',style={'width':'100%', 'height':'500px'})
                    ])
                    ],style={'margin':'2em'}),
                
            html.Div([  #SECTION 5
                html.Div([ #ALLOCATION GRAPH
                    dcc.Graph(id='allocation_graph',
                    figure = px.bar(allocation_df, x="Allocation", y="Symbol",
                    title="Portfolio Allocation", text_auto='.2s'))
                    ],style={'width':'50%', 'display':'inline-block'}),

                html.Div([ #SECTOR GRAPH
                    dcc.Graph(id='sector_graph',
                    figure = px.histogram(sector_df, x="Allocation", y="Sector", title="Investment Share by Sector", 
                    barmode='group', text_auto='.2s', labels={"Allocation": "Share Percentage"}))
                    ], style={'width':'50%' ,'display':'inline-block'})
                    ], className="row"),

            html.Div([  #SECTION 6
                dcc.Dropdown(['Daily', 'Total'], 'Daily', id='dropdown-selection-sector-returns'), #DAILY/TOTAL PROFIT BY SECTOR
                dcc.Graph(id='graph-sector-returns')
                ]),
                
            html.Div([ #SECTION 7
                html.Div([  #INVESTOR TABLE
                    html.H3("Investor Information"),    
                    dash_table.DataTable(investor_df.to_dict('records'),style_cell={'fontSize':'large',
                    'height':'74px','verticalAlign': 'middle', 'textAlign':'center'}) #500px / 6 rows
                    ], style={'width':'50%', 'display':'inline-block', 'textAlign':'center'}),

                html.Div([  #INVESTOR PIE CHART
                    html.H3("Investor Share of Total Funds", style={'position':'relative', 'bottom':'30%', 'textAlign':'center'}),
                    dcc.Graph(id='investor-pie-chart',
                    figure = px.pie(investor_df_og, values='% Total Fund', names='Investor', hole=.6))
                ], style={'width':'50%', 'display':'inline-block'})
            ], className='row'),

            html.Div([
                html.Div([
                    html.H3("Risk and Allocation"),
                    dash_table.DataTable(risk_table_df.to_dict('records'), 
                    style_cell={'fontSize':'large','height':'74px','verticalAlign': 'middle', 'textAlign':'center'},
                    style_data_conditional=[
                {
                    'if': {'filter_query': '{To reduce/add} >= ₹0', 'column_id':'To reduce/add'},
                    'color': 'green'
                },
                {
                    'if': {'filter_query': '{To reduce/add} < ₹0', 'column_id':'To reduce/add'},
                    'color': 'red'
                }
                
                ])
                ])
                ]),
        
            dcc.Interval( 
                id='interval-component',
                interval=30*1000, # in milliseconds
                n_intervals=0)
            ]
            )
    prevent_initial_call='initial_duplicate'

    @dash_app.callback(Output('returns', 'style'),
        Input('interval-component', 'n_intervals'))

    def update_div_style(n):
        new_portfolio = xw.books['Portfolio.xlsx']
        todays_returns = 100 * new_portfolio.sheets['Portfolio']['A13'].value
        if todays_returns < 0:
            return {'color': 'red'}
        else:
            return {'color': 'green'}

    @dash_app.callback(Output('live-update-price_portfolio', 'style'),
        Input('interval-component', 'n_intervals'))

    def update_div_style(n):
        new_portfolio = xw.books['Portfolio.xlsx']
        todays_returns = 100 * new_portfolio.sheets['Portfolio']['A13'].value
        if todays_returns < 0:
            return {'color': 'red'}
        else:
            return {'color': 'green'}

    # Callback to update the current price
    @dash_app.callback(Output('live-update-price-nifty', 'children'),
                Input('interval-component', 'n_intervals'))

    def update_live_price(n):
        ticker_data = yf.Ticker('^NSEI')
        current_price = ticker_data.get_info()['regularMarketPrice']
        current_price = f"{current_price:,.2f}"

        return html.H3(f"₹ {current_price}")

    @dash_app.callback(Output('live-update-price_portfolio', 'children'),
                Input('interval-component', 'n_intervals'))

    def update_live_price(n):
        current_price = update_portfolio_dashboard(stock_names, quantity_list)
        current_price= f"{current_price:,.2f}"
        
        return html.H3(f"₹ {current_price}")


    @dash_app.callback(Output('live-update-nav','children'),
                Input('interval-component', 'n_intervals'))

    def display_nav(n):
        new_portfolio = xw.books['Portfolio.xlsx']
        nav = new_portfolio.sheets['Portfolio']['A25'].value
        nav = f"{nav:.2f}"
        return html.H3(f"{nav}")

    @dash_app.callback(Output('graph-content', 'figure'),
        Input('interval-component', 'n_intervals'),
        Input('dropdown-selection','value'))

    def nifty_and_nav(n, value):
        new_portfolio = xw.books['Portfolio.xlsx']
        minimum = start_date
        stocks_download = yf.download({TICKER_SYMBOL}, start=start_date)
        stocks_download.reset_index(inplace=True)
        stocks_download = stocks_download[['Date', 'Close']]

        last_row = new_portfolio.sheets['Log'].range('D1048576').end('up').row 
        log_df = new_portfolio.sheets['Log'].range('C4:I'+str(last_row)).options(pd.DataFrame, header=1, index=False).value
        trace1 = go.Scatter(x=log_df['Date'],y=log_df['NAV'],mode='lines+markers',name='NAV', line_color ='#2596be')
        trace2 = go.Scatter(x=stocks_download['Date'],y=stocks_download['Close']['^NSEI'], 
            mode='lines+markers',name='NIFTY 50', yaxis='y2', line_color='#be4d25') # yaxis='y2' for dual-axis
        if value == 'NAV':
            figure = go.Figure(data=[trace1])
            figure.update_layout(yaxis_title="Portfolio")
        
        elif value == 'NIFTY 50':
            figure = go.Figure(data=[trace2])
            figure.update_layout(yaxis2=dict(title="NIFTY 50",overlaying="y", side="right"))
        
        else: 
            figure = go.Figure(data=[trace1, trace2])
            figure.update_layout(
            title="Sales and Profit by Month",
            xaxis_title="Time",
            yaxis_title="NAV",
            yaxis2=dict(
            title="NIFTY 50",
            overlaying="y",
            side="right"
            ),showlegend=False)

        figure.layout.paper_bgcolor = colors['background']
        figure.update_layout(title="NAV and NIFTY 50's Performance", xaxis_title="Time")
        return figure

    @dash_app.callback(Output('graph-sector-returns','figure'),
                        Input('dropdown-selection-sector-returns', 'value'))

    def sector_returns(value):
        if value == 'Daily':
            figure = px.histogram(sector_returns_df, x="Sector", y="Today Profit and Loss (Percentage)", 
            title="Today's Returns by Sector", 
            barmode='group', text_auto='.2s')
            figure.update_traces(marker_color='#9925be')
        else:
            
            figure = px.histogram(sector_returns_df, x="Sector", y="Total Profit and Loss (Percentage)", title="All-time Returns by Sector", 
            barmode='group', text_auto='.2s')
        figure.layout.paper_bgcolor = colors['background']
        figure.update_layout(yaxis_title="Profit and Loss in %")
        return figure

    @dash_app.callback(Output('time', 'children'),
                Input('interval-component', 'n_intervals'))

    def update_time(n):
        date_and_time = datetime.datetime.now()
        date_and_time = date_and_time.strftime('%d/%m/%Y %I:%M:%S %p')
        return html.H4(f"Last updated on: {date_and_time}", style={'fontWeight': 'normal'})

    @dash_app.callback(Output('returns', 'children'),
                Input('interval-component', 'n_intervals' ))

    def returns_display(n):
        new_portfolio = xw.books['Portfolio.xlsx']
        #todays_returns = new_portfolio.sheets['Portfolio']['A13'].value
        todays_returns = new_portfolio.sheets['Portfolio']['A13'].value
        todays_returns = f"{todays_returns:.2%}"
        return html.H3(f"{todays_returns}")

    #if __name__ == '__main__':
    #   app.run(debug=True)

    """def update_portfolio_dashboard(stock_names,quantity_list):
        new_portfolio = xw.books['Portfolio.xlsx']
        current_price, investment_value, total_profit_loss = [[] for i in range(3)]
        portfolio_sum = float(new_portfolio.sheets['Funds_Portfolio']['A7'].value)
        #money_invested_sum = new_portfolio.sheets['Funds_Portfolio']['I11'].value
        total_profit = float(new_portfolio.sheets['Funds_Portfolio']['A10'].value)
        i =0
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
        return portfolio_sum"""

    return dash_app