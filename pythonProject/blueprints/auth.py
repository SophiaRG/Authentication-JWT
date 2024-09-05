from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector as mysql
import jwt
import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utilities.db_util import convert_db_data_in_list_dict
from utilities.token_util import confirm_token, generate_confirmation_token

load_dotenv()

auth_bp = Blueprint('auth', __name__)

mydb = mysql.connect(
        user=os.environ.get('MYSQL_USER'),
        password=os.environ.get('MYSQL_PASSWORD'),
        database=os.environ.get('MYSQL_DATABASE'),
        port=os.environ.get('MYSQL_PORT'),
        host=os.environ.get('MYSQL_HOST'),
    )

mycursor = mydb.cursor()

mycursor.execute("""CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                username VARCHAR(255), 
                email VARCHAR(255), 
                password VARCHAR(255));""")


@auth_bp.route("/register", methods=["POST", "GET"])
def register_user():
    if request.method == "POST":
        try:
            username = request.json.get("username")
            email = request.json.get("email")
            password = request.json.get("password")
        except:
            return {
                "message": "Invalid requested data!",
                "data": None,
                "error": "Unauthorized"
                }, 400
        mycursor.execute("SELECT * FROM users WHERE email = %s", (email, ))
        account = mycursor.fetchall()

        if account:
            return {
                "message": "Account already exist!",
                "data": None,
                "error": "Conflict"
            }, 409
        else:
            hash_and_salted_password = generate_password_hash(
                password,
                method='pbkdf2:sha256',
                salt_length=8
            )
    
        token = generate_confirmation_token(email)
        print(token)

        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        new_user = (username, email, hash_and_salted_password)
        mycursor.execute(sql, new_user)
        mydb.commit()

        return jsonify({"Message": "You successfully registered"}), 201


    return jsonify({"Message": "Register or login first"}), 200


@auth_bp.route("/login", methods=["POST", "GET"])
def login_user():
    if request.method == "POST":
        try:
            email = request.json.get("email")
            password = request.json.get("password")
        except:
            return jsonify({
                "message": "Invalid request message!!",
                "data": None,
                "error": "Bad request"
            }), 400
        
        try:
            mycursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
            user = convert_db_data_in_list_dict(mycursor)
            if not user:
                raise ValueError("User does not exist.")
        except Exception as e:
            return jsonify({
                "message": str(e),
                "data": None,
                "error": "Does not exist"
            }), 404
        
        ps_hash = str(user[0]["password"])

        try: 
            if not check_password_hash(ps_hash, password=password):
                raise ValueError("Invalid password")
        except Exception as e:
            return jsonify({
                "message": str(e),
                "data": None,
                "error": "Unauthorized"
            }), 400
        

        if user and check_password_hash(ps_hash, password=password):
            access_token = jwt.encode({"email": email}, key=os.environ["SECRET_KEY"])
            print(access_token)
            return jsonify({
                "message": "Logged in",
                "token": {
                    "access": access_token,
                }
            }), 200
        
    return jsonify({"Message": "Register or login first."}), 200

