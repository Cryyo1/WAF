from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
import json
import os 
import hashlib
import socket
from flask_cors import CORS
from flask import make_response
from dotenv import load_dotenv
import datetime
load_dotenv()
app = Flask(__name__)
cors=CORS(app, resources={r"/*": {"origins": "*"}})
#setting content type to json
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["JWT_SECRET_KEY"]=os.getenv("JWT_SECRET_KEY")

jwt=JWTManager(app)


current_user={
    "name":"",
    "email":"",
    "profilePicture":"",
}

@app.route('/undefined/api/hello', methods=["GET"])
def Hello():
    with open('./data/graphData.json', 'r') as jsonFile:
        data = json.loads(jsonFile.read())
    today=datetime.date.today()
    lastdate=datetime.datetime.strptime(data[6]["date"],"%Y-%m-%d").date()
    
    if lastdate < today :
        data[6]["date"]=str(today)
        data[6]["requests"]=0
        with open('./data/graphData.json','w') as jsonFile:
            json.dump(data,jsonFile,indent=2)

    return "Hello World"
@app.route('/status', methods=["GET"])
def status():
    status={
        "ip":"127.0.0.1",
        "port":"8080",
        "status":""
    }
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    result=sock.connect_ex(('localhost',8080))
    status["status"]="Up" if result==0 else "Down"
    return jsonify(status)


@app.route('/api/login', methods=["POST"])
def create_token():
    with open('./data/users.json', 'r') as jsonFile:
        users=json.loads(jsonFile.read())
        
    email=request.json.get("email",None)
    password=request.json.get("password",None)

    print(email,password,"True")
    
    for user in users:
        if user["email"] == email and user["password"] == hashlib.sha256(password.encode()).hexdigest():
            access_token = create_access_token(identity=email)
            response = {"access_token":access_token,}
            current_user["name"]=user["name"]
            current_user["email"]=email
            current_user["profilePicture"]=user["Profile Picture"]
            return response,200

    return {"msg": "Bad email or password"},401
    

@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@app.route("/user", methods=['GET'])
def users():
    return jsonify(current_user)
@app.route('/requests', methods=['GET'])
def requests():
    with open('./data/requests.json', 'r') as jsonFile:
        data = json.loads(jsonFile.read())
    response=jsonify(data)
    return response

@app.route('/data', methods=['GET'])
def graphData():
    with open('./data/graphData.json', 'r') as jsonFile:
        data = json.loads(jsonFile.read())
    response=jsonify(data)
    return response
# Gestion des données 
@app.route('/insert' , methods=['POST'])
def insert():
    post_data=request.data
    post_data=json.loads(post_data.decode('utf-8'))
    with open('./data/requests.json', 'r') as jsonFile:
        data = json.loads(jsonFile.read())
    data.insert(0,post_data)
    with open('./data/requests.json','w') as jsonFile:
        json.dump(data,jsonFile,indent=2)
    
    if post_data["Class"] == "Anormale":
        with open('./data/graphData.json', 'r') as jsonFile:
            data = json.loads(jsonFile.read())
        data[6]["requests"]+=1
        data[6][post_data["Type"].lower()]+=1
        with open('./data/graphData.json','w') as jsonFile:
            json.dump(data,jsonFile,indent=2)
        
    return 'Data inserted'


if __name__ == '__main__':
    app.run(debug=True)