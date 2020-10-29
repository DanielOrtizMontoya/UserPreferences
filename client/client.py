import pika
import sys
import json

def read_parameters():
    global ACTION 
    global OPERATION_ID
    global USER_ID

    ACTION = ""
    OPERATION_ID = ""
    USER_ID = ""
   
    try:
        ACTION = sys.argv[1]
    except IndexError:
        print("[x][client] No action")
        exit()

    try:
        USER_ID = sys.argv[2]
    except IndexError:
        print("[x][client] No user ID")
        exit()
        
    try:
        OPERATION_ID = int(sys.argv[3])
    except IndexError:
        print("[x][client] No ID operation")
        exit()
        
    if(ACTION != "loan" and ACTION != "transfer"):
        print("[x][client] invalid action (use loan or transfer)")
        exit()
        
def take_action():
    if(ACTION == "loan"):
        send_rabbitmq("loan", create_loan_message())
    elif(ACTION == "transfer"):
        send_rabbitmq("transfer", create_transfer_message())
        
def send_rabbitmq(action,message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')  
    key = "UserPreferencesServiceInput"
      
    channel.basic_publish(
        exchange='direct_logs', routing_key=key, body=message)
    print("[*][client] " + action + " was send")

    connection.close()

def create_loan_message():
    
    message = json.dumps({
        "type": "loan",
        "data":[
            {
                "customerInformation":{
                    "documentNumber":USER_ID,
                    "idType":"CC"               
                    },
                "LoanInformation":{
                    "loanNumber":OPERATION_ID,
                    "participationNumber":12345,
                    "paymentDate":"2001-10-26T21:32:52",
                    "paymentType":"Pago Total o cancelacion",
                    "accountType":"D",
                    "accountNumber":1234567890123456,
                    "PaymentValue":1245677,
                    "depositTransactionCode":123458,
                    "transactionDescriptionInDeposits":"se realizo la transaccion de manera exitosa",
                    "transactionTrackingNumber":"000087888"           
                    }     
                }
            ]   
        })
    
    return message

def create_transfer_message():
    
    message = json.dumps({
        "type": "transfer",
        "data":[
            {
                "customerInformation":{
                    "documentNumber":USER_ID,
                    "idType":"CC"               
                    },
                "transferInformation":{
                    "transferNumber":OPERATION_ID,
                    "participationNumber":12345,
                    "paymentDate":"2001-10-26T21:32:52",
                    "paymentType":"Pago Total o cancelacion",
                    "accountType":"D",
                    "accountNumber":1234567890123456,
                    "PaymentValue":1245677,
                    "destinationAccount":123458,
                    "transactionDescriptionInDeposits":"se realizo la transaccion de manera exitosa",
                    "transactionTrackingNumber":"000087888"           
                    }     
                }
            ]   
        }) 
    
    return message
    
def run():
    read_parameters()
    take_action()

if __name__ == '__main__':
    run()
    


