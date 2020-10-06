import pika
import sys
import json

def read_parameters():
    global ACTION 
    global CLIENT_NAME
    global BANKING_SERVICE
    ACTION = ""
    CLIENT_NAME = ""
    BANKING_SERVICE = ""
    
    try:
        ACTION = sys.argv[1]
    except IndexError:
        print("[x][client] No action")
        exit()
        
    if(ACTION != "write" and ACTION != "read"):
        print("[x][client] invalid action (use write or read)")
        exit()
        
    try:
        CLIENT_NAME = sys.argv[2]
    except IndexError:
        print("[x][client] No client name")
        exit()
        
    try:
        BANKING_SERVICE = sys.argv[3]
    except IndexError:
        pass

def take_action():
    if(ACTION == "write"):
        if(BANKING_SERVICE):
            send_rabbitmq(ACTION)
        else:
            print("[x][client] No banking service")
            exit()
    else: send_rabbitmq(ACTION)
    
def send_rabbitmq(action):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
    
    key = "UserPreferencesServiceInput"
    message = json.dumps({
        "action": action,
        "clientName": CLIENT_NAME,
        "bankingService": BANKING_SERVICE      
    })
    
    channel.basic_publish(
        exchange='direct_logs', routing_key=key, body=message)
    print("[*][client] " + action + " was send")

    connection.close()
    

def run():
    read_parameters()
    take_action()

if __name__ == '__main__':
    run()
    


