# Portfolio Manager Application (stocks_app)

This project was undertaken to help automate processes for a friend's portfolio documentation, which was being maintained on an Excel workbook. The results of this full-stack application are a reduction in the amount of time he spends maintaining the portfolio daily by 85% and an increase in the accuracy of the portfolio by reducing human error.

An Excel workbook with dummy data (Portfolio.xlsx) has been provided for test purposes. In order to create an actual workbook to maintain a portfolio, refer to the earlier iteration of this project [Stocks_Portfolio_Dashboard](https://github.com/OP-9/Stocks_Portfolio_Dashboard).

<img width="1440" height="812" alt="Screenshot 2026-02-26 at 11 35 21 AM" src="https://github.com/user-attachments/assets/a3c75b24-279b-49c5-b461-15e2e9a1a8ee" />


## Setup

1. Configure an .env file with the following variables:
   - PATH_NAME = relative path of the portfolio workbook in the "data" folder.
   - WB_NAME = the name of the workbook, including its extension
2. Open Docker
3. Open the Excel workbook and manually save the file every time before running the app. This ensures that cells with formulae will store results in its cache.
4. Utilise Docker and run the following commands in the IDE terminal:
   - docker compose build
   - docker compose run
   - docker compose down (use this when you want to shut down the app).

"docker compose build" is the command to be run upon running the application for the first time, after which "docker compose run" can be utilised whenever the app needs to be run.

## Warnings

Do not open the Excel workbook while the application is running. This app uses Openpyxl and the chance of corrupting the workbook if it's open while the app is running is high.
