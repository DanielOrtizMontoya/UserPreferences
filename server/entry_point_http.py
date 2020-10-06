import controller as ct
from flask import Flask, request, jsonify
password = "1234"


app = Flask(__name__)

@app.route('/test', methods=['GET','POST'])
def test():
    if request.method == "GET":
        req_Json = request.json
        clientName = req_Json['clientName']
        res_msg = ""
        first_preference = ""
        second_preference = ""
        third_preference = ""
        
        if(ct.check_client_exists(password, clientName)):
            res_msg = "successful"
            first_preference, second_preference, third_preference = ct.client_preferences(password, clientName)
        else:
            res_msg = "client not found"
        
        return jsonify({"response":res_msg,
                        "first_preference":first_preference,
                        "second_preference":second_preference,
                        "third_preference":third_preference})
    
    elif request.method == "POST":
        req_Json = request.json
        clientName = req_Json['clientName']
        bankingService = req_Json['bankingService']
        
        ct.client_connected(password,clientName,bankingService)
        
        return jsonify({"response":"registered"})

if __name__ == '__main__':
    app.run(debug=True, port=9090)


    