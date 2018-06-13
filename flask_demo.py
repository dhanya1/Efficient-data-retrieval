import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# App configurations
db_file = os.path.abspath('advertima.db')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+db_file
db = SQLAlchemy(app)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)
