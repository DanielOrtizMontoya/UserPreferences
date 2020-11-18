import pika
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
        queue=queue_name, on_message_callback=callback_new_event, auto_ack=True)
    
    channel.start_consuming()
    
def callback_new_event(ch, method, properties, body):  
    ct.client_event(PASSWORD_DB,body)
                         
def run():
    read_password_db()
    connect_rabbitmq()
       
if __name__ == '__main__':
    run()

