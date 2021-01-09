import os

from docviz_app import app

if __name__ == "__main__":
    #app.run_server(debug=True, host=os.getenv("APP_HOST", "127.0.0.1"))
    app.run_server(debug=True, host='0.0.0.0', port='8080')