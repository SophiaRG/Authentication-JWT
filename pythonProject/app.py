import mysql.connector
from flask import Flask, request
from blueprints.auth import auth_bp
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

mydb = mysql.connector.connect(
    user=os.environ.get('MYSQL_USER'),
    password=os.environ.get('MYSQL_PASSWORD'),
    database=os.environ.get('MYSQL_DATABASE'),
    port=os.environ.get('MYSQL_PORT'),
    host=os.environ.get('MYSQL_HOST'),
)
mycursor = mydb.cursor()

app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route("/")
def home():
    return "Hello"

if __name__ == "__main__":
    app.run(debug=True)