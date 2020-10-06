import pika
import json

def connect_rabbitmq():
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
    message = json.loads(body)
    
    print("--  welcome {} --".format(message["clientName"]))
    print(" ")
    print("*********************************")
    print("*******     {}     **********".format(message["pref_1"]))
    print("*********************************")
    print(" * {}" .format(message["pref_2"]))
    print(" * {}" .format(message["pref_3"]))

def run():
    connect_rabbitmq()
       
if __name__ == '__main__':
    run()




