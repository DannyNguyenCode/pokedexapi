from flask import Flask, request,jsonify
from app import crud,services
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route("/users/create",methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        user_exists = crud.get_user_by_email(data["email"])
        if user_exists:
            return jsonify({"message":f"{data['email']} already exists in the database"}),409
        data["password"]= services.hash_password(data.get("password"))
        response = crud.create_user(data)
        return jsonify(response),201
    except Exception as error:
        return jsonify({"error":f"{error}"}),500
    
@app.route("/users",methods=["GET"])
def list_users():
    try:
        email = request.args.get('email')
        if email:
            response = crud.get_user_by_email(email)
            return jsonify([res.to_dict() for res in response]),200
        else:
            responses = crud.list_users()
            return jsonify([response.to_dict() for response in responses]),200
    except Exception as error:
        return jsonify({"error":f"{error}"}),500

@app.route("/users/<string:id>",methods=["GET"])
def get_user_by_id(id):
    try:
        response = crud.get_user_by_id(id)
        if not response.exists:
            return jsonify({"error":f"user with {id} does not exist in database"}),404
        return jsonify(response.to_dict()),200
    except Exception as error:
        return jsonify({"error":f"{error}"}),500
    
@app.route("/users/<string:id>",methods=["PUT"])
def update_user(id):
    try:
        doc = crud.get_user_by_id(id)
        if not doc.exists:
          return jsonify({"error":f"user with {id} does not exist in database"}),404
        data = request.get_json()
        response = crud.update_user(id,data)

        return jsonify(response),200
    except Exception as error:
        return jsonify({"error":f"{error}"}),500
    
@app.route("/users/<string:id>",methods=["DELETE"])
def delete_user(id):
    try:
        doc = crud.get_user_by_id(id)
        if not doc.exists:
          return jsonify({"error":f"user with {id} does not exist in database"}),404
        response = crud.delete_user(id)

        return jsonify(response),200
    except Exception as error:
        return jsonify({"error":f"{error}"}),500

@app.route("/user/login",methods=["POST"])
def login_user():
    try:
        data = request.get_json()
        email = data.get("email")
        password= data.get("password")
        response = crud.get_user_by_email(email)
        
        if not response:
            return jsonify({"error":f"User with {email} does not exist in database"}),404

        user = response[0].to_dict()   
        if not services.check_password(password, user["password"]):
            return jsonify({"error":"User email or password is not valid"}),401
        
        token = services.generate_jwt({
            "user_id": response[0].id,
            "email": email
        })
        return jsonify({
                "message":"User has logged in successfully",
                "status":200,
                "token":token
                }),200
 
    except Exception as error:
        return jsonify({"error":f"{error}"}),500


@app.route("/user/verify_token",methods=["POST"])
def verify_token():
    try:
        data = request.get_json()
        token = data["id_token"]
        decoded = services.verify_token(token)
        if not decoded:
            return jsonify({"error":"user is not verified"}),401
        
        email = decoded["email"].lower()
        uid = decoded.get("uid")
        provider = decoded.get("firebase", {}).get("sign_in_provider")
        existing_user = crud.get_user_by_email(email)
        if not existing_user:
            crud.create_user({
                "email": email,
                "uid": uid,
                "auth_provider": provider
            })
        return jsonify({
            "message":"user is verified",
            "uid": uid,
            "provider":provider
            }),200
    except Exception as error:
        return jsonify({"error":f"{error}"}),500