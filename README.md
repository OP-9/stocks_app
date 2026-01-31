# Portfolio Manager Application (stocks_app)

This project was undertaken to help automate processes for a friend's portfolio documentation, which was being maintained on an Excel workbook. The results of this full-stack application are a reduction in the amount of time he spends maintaining the portfolio daily by 85% and an increase in the accuracy of the portfolio by reducing human error.

An Excel workbook with dummy data (Portfolio.xlsx) has been provided for test purposes. In order to create an actual workbook to maintain a portfolio, refer to the earlier iteration of this project [Stocks_Portfolio_Dashboard](https://github.com/OP-9/Stocks_Portfolio_Dashboard).

<img width="1440" height="823" alt="Screenshot of the Portfolio Application" src="https://github.com/user-attachments/assets/a56a7204-6b85-4e02-b5c5-bb8639e36244" />

## Setup

[Node.js](https://nodejs.org/en/download) is required in order for the application to work.

1. Configure an .env file with the following variables:
   - PATH_NAME = full path of the portfolio workbook
   - WB_NAME = the name of the workbook, including its extension
2. Install the necesary modules through the requirements.txt file (pip install -r requirements.txt)
3. Run run.py
4. In a seperate terminal, run the following command: npm run dev
