from flask import Flask
from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy

# Initialize server
app = Flask(__name__)

# Connect to mysql database
# (uri format: protocol://user:password@host/database)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/main'
# db = SQLAlchemy(app)

# Setup CORS
CORS(app)

@app.route('/')
def index():
    return 'Hello'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')