from flask import Flask, request, jsonify
import json
import pika

def send_rabbitmq(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')  
    key = "UserPreferencesServiceInput"
      
    channel.basic_publish(
        exchange='direct_logs', routing_key=key, body=message)
    print("[*][client] Event sent")

    connection.close()
        
app = Flask(__name__)

@app.route('/event', methods=['POST'])
def event():
    if request.method == "POST":
        req_Json = request.json
        req_message = json.dumps(req_Json)
        send_rabbitmq(req_message)     
        return jsonify({"response":"event sent"})        
        
if __name__ == '__main__':

    app.run(debug=True, port=9090)