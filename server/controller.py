import store
import json

def client_connected(password,clientId,bankingService): 
    db = store.connect_to_neo4j_db(password)
   
    if (store.client_exists(db,clientId)):
        print("[*][controller] client exists")
    else:
        store.create_client_node(db,clientId)
        
    if (store.banking_service_exists(db,clientId,bankingService)):
        store.add_importance_banking_service(db,clientId,bankingService)
    else:
        store.create_banking_service(db,clientId,bankingService)
        store.create_client_banking_relationship(db,clientId,bankingService)

def check_client_exists(password, clientId):
    db = store.connect_to_neo4j_db(password)
    
    if(store.client_exists(db, clientId)):
        return True
    else:
        return False
    
def client_preferences(password, clientId):
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
    