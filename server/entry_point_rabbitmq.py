import pika
import json
import controller as ct
import sys

def read_password_db():
    global PASSWORD_DB
    
    try:
        PASSWORD_DB = sys.argv[1]
    except IndexError:
        print("[x][ep rabbit] Enter the database password")
        exit()

def connect_rabbitmq():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
    
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    
    key = "UserPreferencesServiceInput"
    channel.queue_bind(
        exchange='direct_logs', queue=queue_name, routing_key=key)
    
    print(' [*][ep rabbit] Waiting for logs. To exit press CTRL+C')
                
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    
    channel.start_consuming()
    
def callback(ch, method, properties, body):  
    message = json.loads(body)
    if(message["action"] == "write"):
        write_new_client_and_bankingservice(PASSWORD_DB,
                                            message["clientName"],
                                            message["bankingService"])
    elif(message["action"] == "read"):
        message = read_client_preferences(PASSWORD_DB,
                                          message["clientName"])    
        key = "UserPreferencesServiceOutput"
        ch.basic_publish(
            exchange='direct_logs', routing_key=key, body=message)     
    else: print("[x][ep rabbit] Action null")
    
def write_new_client_and_bankingservice(password,
                                        clientName,
                                        bankingService):
    ct.client_connected(password,clientName,bankingService) 
    print("[*][ep rabbit] Successful registration")
           
def read_client_preferences(password, clientName):
    action = "response"
    if(ct.check_client_exists(password, clientName)):
        pref_1, pref_2, pref_3 = ct.client_preferences(password, clientName)
        
        message = json.dumps({
            "action": action,
            "clientName": clientName,
            "pref_1": pref_1,
            "pref_2": pref_2,
            "pref_3": pref_3,     
        })              
    else:
        print("[x][ep rabbit] Client not found") 

        message = json.dumps({
            "action": "not found",
            "clientName": "not found",
            "pref_1": "not found",
            "pref_2": "not found",
            "pref_3": "not found",     
        })
        
    return message
                
def run():
    read_password_db()
    connect_rabbitmq()
       
if __name__ == '__main__':
    run()

