from flask import Blueprint, request, jsonify

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data.get("email")
    password = data.get("password")

    if email == "admin@gmail.com" and password == "123456":

        return jsonify({
            "success": True,
            "message": "Login Successful"
        })

    return jsonify({
        "success": False,
        "message": "Invalid Credentials"
    })