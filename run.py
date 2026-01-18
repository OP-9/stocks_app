from flask_file import app
from waitress import serve

if __name__ == '__main__':
    print("\nStarting app...\n")
    #app.run(debug=True, port=5000)
    print(" Server is running on http://localhost:5173")
    
    #Production WSGI server
    serve(app, host='localhost', port=5000)

