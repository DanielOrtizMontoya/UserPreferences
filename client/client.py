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
    
def read_rabbitmq_response():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
    
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    
    key = "UserPreferencesServiceOutput"
    channel.queue_bind(
        exchange='direct_logs', queue=queue_name, routing_key=key)
    
    print('[*][ui] Waiting for logs. To exit press CTRL+C')
                
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    
    channel.start_consuming() 

def callback(ch, method, properties, body): 
    global RES_MESSAGE
    RES_MESSAGE = body
    ch.stop_consuming()
    
app = Flask(__name__)

@app.route('/event', methods=['POST'])
def event():
    if request.method == "POST":
        req_Json = request.json
        req_message = json.dumps(req_Json)
        send_rabbitmq(req_message)     
        return jsonify({"response":"event sent"})        
    
@app.route('/preferences/bankingservices', methods=['GET'])
def preferences_bankingservices():
    if request.method == "GET":
        req_Json = request.json
        req_message = json.dumps(req_Json)
        send_rabbitmq(req_message) 
        
        read_rabbitmq_response()
        res_json = json.loads(RES_MESSAGE)  
        return jsonify(res_json)
    
@app.route('/preferences/accounts', methods=['GET'])
def preferences_accounts():
    if request.method == "GET":
        req_Json = request.json
        req_message = json.dumps(req_Json)
        send_rabbitmq(req_message) 
        
        read_rabbitmq_response()
        res_json = json.loads(RES_MESSAGE)  
        return jsonify(res_json)
    
if __name__ == '__main__':

    app.run(debug=True, port=9090)