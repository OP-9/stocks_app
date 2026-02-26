import dash
from dash.dependencies import Output, Input
from dash import dcc, html, dash_table
import dash_loading_spinners as dls
import plotly.express as px
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import openpyxl
import datetime
import logging
from zoneinfo import ZoneInfo

logger = logging.getLogger('backend')

from excel_connector import Portfolio, timezone

portfolio = Portfolio()

try:
    wb = portfolio.safe_load()

    result = portfolio.excel_reader()

    if result == 1:
        print("Error reading Excel workbook. Please manually save the workbook before running this app.")
    elif result == 0:
        print("Successfully read Excel workbook!")
    
    start_date = wb['Portfolio']['A17'].value
    start_date = start_date.strftime('%Y-%m-%d')

    portfolio_df = portfolio.portfolio_df

    combined_sector_df = portfolio.combined_sector_df

    combined_sector_df['Allocation'] = pd.to_numeric(combined_sector_df['Allocation'], errors='coerce')
    
    combined_allocation_df = portfolio.combined_allocation_df
    
                                                                                  
    #ADDING CUSTOM FONT 
    external_stylesheets = ['https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=Montserrat:ital,wght@0,100..900;1,100..900&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap']

    def create_dash_app(flask_app):
        
        logging.debug("Entering create_dash_app")

        dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dashboard/", external_stylesheets=external_stylesheets)


        #Alter colours of general layout, cards, and header
        colors = {
            'background': 'white',
            'text': 'black',
            'card_background': 'white'
        }

        card_style = {
            'backgroundColor': colors['card_background'],
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '2px 4px 8px #31473a',
            'marginBottom': '20px'
        }

        header_style = {
            'backgroundColor': '#31473a',
            'color': 'white',
            'padding': '20px',
            'borderRadius': '10px',
            'marginBottom': '30px'
        }
        
        #Loading symbol style
        spinner_type = "dot"
        spinner_color = "#31473a"

        # Ticker symbol to track
        TICKER_SYMBOL = '^NSEI'

        nifty = yf.Ticker(TICKER_SYMBOL)
        name = nifty.info['shortName']


        dash_app.layout = html.Div(style={'fontFamily': 'Poppins, Lato, Roboto, sans-serif', 
        'backgroundColor': colors['background'], 'margin':'2%', 'marginBottom':'5rem'},
        children = [

            html.Div([ #SECTION 1, TITLE
                html.Div([
                    html.H1("Stocks Portfolio Dashboard", style={'textAlign':'center'})
                    ]),
                    html.Div([ #SECTION 1, TIME
                        html.Div(id='time')
                    ], style={'textAlign':'center'})
                    ],style=header_style),

                html.Div([ #SECTION 2
                        dcc.Loading(
                        children=[
                            html.Div([  # LIVE DISPLAY OF PORTFOLIO
                            html.H3("Portfolio Value"),
                            html.Div(id='live-update-price_portfolio'),
                            ],style={**card_style, 'textAlign': 'center', 'color': 'black',})], type=spinner_type
                            , color = spinner_color),
                        
                        dcc.Loading(
                        children=[
                            html.Div([  # LIVE DISPLAY OF RETURNS
                                html.H3("Total Return"),
                                html.Div(id='returns',),
                                ],style={**card_style, 'textAlign': 'center', 'color': 'black',}
                                )], type=spinner_type, color = spinner_color),
                        
                        dcc.Loading(
                        children=[
                            html.Div([
                            html.H3("Live Price of NIFTY 50"),
                            html.Div(id='live-update-price-nifty') #NIFTY 50 PRICE UPDATE
                            ],style={**card_style, 'textAlign': 'center', 'color': 'black',})],
                            type=spinner_type, color = spinner_color),
                        
                        dcc.Loading(
                        children=[
                            html.Div([
                                html.H3("Current NAV"),
                                html.Div(id='live-update-nav'), #NAV UPDATE
                                ],style={**card_style, 'textAlign': 'center', 'color': 'black',})], type=spinner_type, 
                                color = spinner_color)
                        
    
                ],style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 
                'gap': '20px','marginBottom': '30px'}),

                html.Div([ #SECTION 3
                    html.Div([  #TITLE OF GRAPHS
                        html.H3("Performance of NAV and NIFTY 50")
                        ],style={'textAlign':'center'}),

                    
                    html.Div([  #GRAPH
                        dcc.Dropdown(['NAV', 'NIFTY 50', 'NAV & NIFTY 50'], 'NAV & NIFTY 50', id='dropdown-selection'),
                        dcc.Loading(
                        dcc.Graph(id='graph-content',style={'width':'100%', 'height':'500px'})
                        , type=spinner_type , color = spinner_color)
                        ])
                        ],style={'margin':'2em'}),
                    
                html.Div([  #SECTION 5
                    html.H3("Allocation & Sector Graphs"),

                    html.Div([ #ALLOCATION GRAPH
                        dcc.Graph(id='allocation_graph',
                        figure = px.bar(combined_allocation_df, x="Allocation", y="Symbol",
                        title="Portfolio Allocation", text_auto='.2s'))
                        ],style={'width':'50%', 'height':'40rem','display':'inline-block'}),

                    html.Div([ #SECTOR GRAPH
                        dcc.Graph(id='sector_graph',
                        figure = px.histogram(combined_sector_df, x="Allocation", y="Sector", title="Investment Share by Sector", 
                        barmode='group', text_auto='.2s'))
                        ], style={'width':'50%', 'height':'40rem','display':'inline-block'}, )
                        ], className="row", style={'textAlign':'center'}),

                html.Div([  #SECTION 6
                        html.Div([
                            html.H3("Returns")
                        ], style={'textAlign':'center'}),

                        dcc.Loading(
                        html.Div([
                        dcc.Dropdown(['Daily', 'Total'], 'Daily', id='dropdown-selection-sector-returns'), #DAILY/TOTAL PROFIT BY SECTOR
                        dcc.Graph(id='graph-sector-returns')]), type='graph', color = spinner_color)
                    ]),
                    
                html.Div([ #SECTION 7
                     #INVESTOR TABLE
                        html.H3("Investor Information"), 

                        dcc.Loading(
                        html.Div([dash_table.DataTable(style_cell={'fontSize':'large',
                        'height':'74px','verticalAlign': 'middle', 'textAlign':'center'}, id = "investor_table")])
                        , type='circle', color = spinner_color)
                        
                    ], style={'textAlign':'center', 'margin':'3rem 2rem 3rem'}), #500px / 6 rows

                html.Div([
                        html.H3("Risk and Allocation"),

                        dcc.Loading(
                        html.Div
                        ([dash_table.DataTable(
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
                        ], id = 'risk_table')]), type='circle', color = spinner_color)
                    ], style={'textAlign':'center', 'margin': '3rem 2rem 2rem'}),
            
                dcc.Interval( 
                    id='interval-component',
                    interval=150*1000, # in milliseconds
                    n_intervals=0)
                ]
                )
                

        prevent_initial_call='initial_duplicate'

        @dash_app.callback(
            [Output('live-update-price_portfolio', 'style'),
            Output('returns', 'style')],
            Input('interval-component', 'n_intervals'))

        def update_div_style(n):
            wb = portfolio.safe_load()
            portfolio_return_perc = float(wb['Portfolio']['A4'].value/wb['Portfolio']['A7'].value - 1)

            portfolio_return_perc = 100 * float(wb['Portfolio']['A4'].value/wb['Portfolio']['A7'].value - 1)
            if portfolio_return_perc < 0:
                return {'color': 'red'}, {'color': 'red'}
            else:
                return {'color': 'green'}, {'color': 'green'}


        # Callback to update the current price
        @dash_app.callback(Output('live-update-price-nifty', 'children'),
                    Input('interval-component', 'n_intervals'))

        def update_live_price(n):
            ticker_data = yf.Ticker('^NSEI')
            current_price = ticker_data.get_info()['regularMarketPrice']
            current_price = f"{current_price:,.2f}"

            return html.H3(f"₹ {current_price}")

        @dash_app.callback(
            [Output('live-update-price_portfolio', 'children'),
            Output('returns', 'children'),
            Output('live-update-nav','children')],
                    Input('interval-component', 'n_intervals'))

        def update_live_price(n):
            current_price, todays_returns, nav = portfolio.update_portfolio_dashboard()
            current_price= f"{current_price:,.2f}"
            nav = f"{nav:.2f}"
            todays_returns = f"{todays_returns:.2%}" 
            
            return html.H3(f"₹ {current_price}"), html.H3(f"{todays_returns}"), html.H3(f"{nav}")


        @dash_app.callback(Output('graph-content', 'figure'),
            Input('interval-component', 'n_intervals'),
            Input('dropdown-selection','value'))

        def nifty_and_nav(n, value):
            minimum = start_date
            stocks_download = yf.download({TICKER_SYMBOL}, start=start_date)
            stocks_download.reset_index(inplace=True)
            stocks_download = stocks_download[['Date', 'Close']]

            log_df = portfolio.log_df
            
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
            portfolio_df = portfolio.portfolio_df
            combined_sector_returns_df = portfolio.combined_sector_returns_df
            
            if value == 'Daily':
                figure = px.histogram(combined_sector_returns_df, x="Sector", y="Today Profit and Loss (Percentage)", 
                title="Today's Returns by Sector", 
                barmode='group', text_auto='.2s')
                figure.update_traces(marker_color='#9925be')

            else:
                figure = px.histogram(combined_sector_returns_df, x="Sector", y="Total Profit and Loss (Percentage)", title="All-time Returns by Sector", 
                barmode='group', text_auto='.2s')
            figure.layout.paper_bgcolor = colors['background']
            figure.update_layout(yaxis_title="Profit and Loss in %")
            return figure


        @dash_app.callback(Output('sector_graph','figure'),
                            Input('interval-component', 'n_intervals'))

        def sector_allocation(value):
            combined_sector_df = portfolio.combined_sector_df
            
            figure = px.histogram(combined_sector_df, x="Allocation", y="Sector", 
            title="Investment Share by Sector", 
            barmode='group', text_auto='.2s')
            figure.update_layout(xaxis_ticksuffix='%')
            return figure


        @dash_app.callback(Output('allocation_graph','figure'),
                            Input('interval-component', 'n_intervals'))

        def portf_allocation(value):
            combined_allocation_df = portfolio.combined_allocation_df

            figure = px.bar(combined_allocation_df, x="Allocation", y="Symbol", text='Allocation',
            title="Portfolio Allocation", text_auto='.2s')
            figure.update_traces(texttemplate='%{text:.1f}%')
            return figure


        @dash_app.callback(Output('time', 'children'),
                    Input('interval-component', 'n_intervals'))

        def update_time(n):
            date_and_time = datetime.datetime.now(ZoneInfo(timezone))
            date_and_time = date_and_time.strftime('%d/%m/%Y %I:%M:%S %p')
            return html.H4(f"Last updated on: {date_and_time}", style={'fontWeight': 'normal'})

        

        @dash_app.callback(Output('investor_table', 'data'),
                Input('interval-component', 'n_intervals'))
        def update_investor_table(n):

            investor_df_og = portfolio.investor_df_og
            
            investor_df = investor_df_og[['Investor', 'Amount Invested', 'Investment Value', '% Total Fund','Profit/Loss']].copy() 

            investor_df['Profit/Loss'] = investor_df['Profit/Loss'].map('{:.2%}'.format)
            investor_df['% Total Fund'] = investor_df['% Total Fund'].map('{:.2%}'.format)
            investor_df['Amount Invested'] = investor_df['Amount Invested'].map('₹{:,.2f}'.format)

            investor_df['Investment Value'] = pd.to_numeric(investor_df['Investment Value'], errors='coerce')
            investor_df['Investment Value'] = investor_df['Investment Value'].fillna(0).map('₹{:,.2f}'.format)

                
            return investor_df.to_dict('records')


        @dash_app.callback(Output('risk_table', 'data'),
                    Input('interval-component', 'n_intervals'))
        def update_risk_table(n):

            risk_table_df = portfolio.risk_table_df

            risk_table_df_dash = risk_table_df.copy()

            #logger.info(f"before {risk_table_df_dash['Current %']}")

            risk_table_df_dash['Allocation %'] = pd.to_numeric(risk_table_df_dash['Allocation %'])
            risk_table_df_dash['Allocation %'] = risk_table_df_dash['Allocation %'].fillna(0).astype(float)
            risk_table_df_dash['Allocation %'] = risk_table_df_dash['Allocation %'].map('{:.2%}'.format)
            
            risk_table_df_dash['Current %'] = pd.to_numeric(risk_table_df_dash['Current %'])
            risk_table_df_dash['Current %'] = risk_table_df_dash['Current %'].fillna(0).astype(float)

            risk_table_df_dash['Allocation Value'] = pd.to_numeric(risk_table_df_dash['Allocation Value'])
            risk_table_df_dash['Allocation Value'] = risk_table_df_dash['Allocation Value'].fillna(0).astype(float)
            
            risk_table_df_dash['Current %'] = risk_table_df_dash['Current %'].map('{:.2%}'.format)
            risk_table_df_dash['Allocation Value'] = risk_table_df_dash['Allocation Value'].map('₹{:,.2f}'.format)

            risk_table_df_dash['Current Value'] = pd.to_numeric(risk_table_df_dash['Current Value'])
            risk_table_df_dash['Current Value'] = risk_table_df_dash['Current Value'].fillna(0).astype(float)
            risk_table_df_dash['Current Value'] = risk_table_df_dash['Current Value'].map('₹{:,.2f}'.format)

            risk_table_df_dash['To reduce/add'] = pd.to_numeric(risk_table_df_dash['To reduce/add'])
            risk_table_df_dash['To reduce/add'] = risk_table_df_dash['To reduce/add'].fillna(0).astype(float)
            risk_table_df_dash['To reduce/add'] = risk_table_df_dash['To reduce/add'].map('₹{:,.2f}'.format)
            
            #logger.info(f"after {risk_table_df_dash}")
                
            return risk_table_df_dash.to_dict('records')


        return dash_app
    
except Exception as e:
    print(f"Error with Dash App")
    logger.debug("Error", exc_info=True)
    