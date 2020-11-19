import store
import json

def check_client_exists(password, clientId):
    db = store.connect_to_neo4j_db(password)
    
    if(store.client_exists(db, clientId)):
        return True
    else:
        return False
    
def client_event(password, body):
    db = store.connect_to_neo4j_db(password)
    eventJson = json.loads(body)
    
    clientId=eventJson["data"][0]["customerInformation"]["documentNumber"]
    bankingService = eventJson["type"]
    
    if (store.client_exists(db,clientId)):
        print("[*][controller] client exists")
    else:
        store.create_client_node(db,clientId)
        
    if (store.banking_service_exists(db,clientId,bankingService)):
        store.add_importance_banking_service(db,clientId,bankingService)
    else:
        store.create_banking_service(db,clientId,bankingService)
        store.create_client_banking_relationship(db,clientId,bankingService)    

    according_banking_service(db, eventJson)
    
    message = json.dumps({
        "response": "registered",    
    }) 

    return message    
    
def client_banking_services_preferences(password, body):
    eventJson = json.loads(body)
    
    clientId=eventJson["data"][0]["customerInformation"]["documentNumber"]
    action = "response"
    first_preference = ""
    second_preference = ""
    third_preference = ""
    db = store.connect_to_neo4j_db(password)
    preferences = store.more_important_banking_services(db, clientId)
        
    try:
        third_preference = preferences[2]
    except IndexError:
        pass

    try:
        second_preference = preferences[1]
    except IndexError:
        pass

    try:
        first_preference = preferences[0]
    except IndexError:
        pass
    
    message = json.dumps({
        "action": action,
        "clientId": clientId,
        "pref_1": first_preference,
        "pref_2": second_preference,
        "pref_3": third_preference,     
    }) 

    return message 

def accounts_preferences(password, body):
    eventJson = json.loads(body)
    
    bankingAccount=eventJson["data"][0]["accountInformation"]["accountNumber"]
    action = "response"
    first_preference = ""
    second_preference = ""
    third_preference = ""
    db = store.connect_to_neo4j_db(password)
    preferences = store.more_important_transfer(db,bankingAccount)
        
    try:
        third_preference = preferences[2]
    except IndexError:
        pass

    try:
        second_preference = preferences[1]
    except IndexError:
        pass

    try:
        first_preference = preferences[0]
    except IndexError:
        pass
    
    message = json.dumps({
        "action": action,
        "bankingAccount": bankingAccount,
        "pref_1": first_preference,
        "pref_2": second_preference,
        "pref_3": third_preference,     
    }) 
    
    return message 

def according_banking_service(password, eventJson):
    bankingService = eventJson["type"]
   
    if(bankingService == "loan"):
        write_loan_data(password, eventJson)
        
    elif(bankingService == "transfer"):
        write_transfer_data(password, eventJson)    
    
def write_loan_data(db, data):
    store.create_loan(db,
                      data["data"][0]["customerInformation"]["documentNumber"],
                      data["type"],
                      data["data"][0]["LoanInformation"]["loanNumber"],
                      data["data"][0]["LoanInformation"]["participationNumber"],
                      data["data"][0]["LoanInformation"]["paymentDate"],
                      data["data"][0]["LoanInformation"]["paymentType"],
                      data["data"][0]["LoanInformation"]["accountType"],
                      data["data"][0]["LoanInformation"]["accountNumber"],
                      data["data"][0]["LoanInformation"]["PaymentValue"],
                      data["data"][0]["LoanInformation"]["depositTransactionCode"],
                      data["data"][0]["LoanInformation"]["transactionDescriptionInDeposits"],
                      data["data"][0]["LoanInformation"]["transactionTrackingNumber"],
                      )

def write_transfer_data(db, data):  
    clientId = data["data"][0]["customerInformation"]["documentNumber"]
    accountNumber = data["data"][0]["transferInformation"]["accountNumber"]
    dstAccountNumber = data["data"][0]["transferInformation"]["destinationAccount"]
    
    if(store.banking_account_exists(db,clientId,accountNumber)):
        print("[*][controller] Banking account exists")
    else:
        store.create_banking_account(db,clientId,accountNumber)
        store.create_client_account_relationship(db,clientId,accountNumber)
        
    store.create_transfer(db,
                      clientId,
                      data["type"],
                      data["data"][0]["transferInformation"]["transferNumber"],
                      data["data"][0]["transferInformation"]["participationNumber"],
                      data["data"][0]["transferInformation"]["paymentDate"],
                      data["data"][0]["transferInformation"]["paymentType"],
                      data["data"][0]["transferInformation"]["accountType"],
                      accountNumber,
                      data["data"][0]["transferInformation"]["PaymentValue"],
                      dstAccountNumber,
                      data["data"][0]["transferInformation"]["transactionDescriptionInDeposits"],
                      data["data"][0]["transferInformation"]["transactionTrackingNumber"],
                      )
    
    if(store.transfer_relationship_exists(db,accountNumber,dstAccountNumber)):
        store.add_importance_transfer(db,accountNumber,dstAccountNumber)
    else:
        store.create_transfer_relationship(db,clientId,accountNumber,dstAccountNumber)
    
    
