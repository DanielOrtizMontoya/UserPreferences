from flask import Flask, request, jsonify, abort
import json
import controller as ct
import sys

def read_password_db():
    global PASSWORD_DB
    
    try:
        PASSWORD_DB = sys.argv[1]
    except IndexError:
        print("[x][ep http] Enter the database password")
        exit()
        
app = Flask(__name__)

@app.route('/preferences/services', methods=['GET'])
def preferences_services():
    if request.method == "GET":
        req_json = request.json
        req_message = json.dumps(req_json)
        
        try:
            res_message=ct.client_banking_services_preferences(PASSWORD_DB, req_message)
            res_json = json.loads(res_message) 
            return jsonify(res_json)             
        except:
            return abort(400)
        

@app.route('/preferences/accounts', methods=['GET'])
def preferences_accounts():
    if request.method == "GET":
        req_json = request.json
        req_message = json.dumps(req_json)
        
        try:
            res_message=ct.accounts_preferences(PASSWORD_DB, req_message)
            res_json = json.loads(res_message) 
            return jsonify(res_json) 
        except:
            return abort(400)
        
if __name__ == '__main__':
    read_password_db()
    app.run(debug=True, port=9091)
