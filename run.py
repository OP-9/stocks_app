from flask_file import app
from waitress import serve
from excel_connector import logger


if __name__ == '__main__':
    logger.info("Starting app...\n")
    #app.run(debug=False, port=5000)
    #print("Server is running on http://localhost:5173")
    
    #Production WSGI server
    logger.info("Server is running on http://localhost:5173")
    serve(app, host='localhost', port=5000)

