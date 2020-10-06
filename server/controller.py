import store

def client_connected(password,clientName,bankingService): 
    db = store.connect_to_neo4j_db(password)
   
    if (store.client_exists(db,clientName)):
        print("[*][controller] client exists")
    else:
        store.create_client_node(db,clientName)
        
    if (store.banking_service_exists(db,clientName,bankingService)):
        store.add_importance_banking_service(db,clientName,bankingService)
    else:
        store.create_banking_service(db,clientName,bankingService)
        store.create_client_banking_relationship(db,clientName,bankingService)

def check_client_exists(password, clientName):
    db = store.connect_to_neo4j_db(password)
    
    if(store.client_exists(db, clientName)):
        return True
    else:
        return False
    
        
def client_preferences(password, clientName):
    first_preference = ""
    second_preference = ""
    third_preference = ""
    db = store.connect_to_neo4j_db(password)
    preferences = store.more_important_banking_services(db, clientName)
        
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

    return first_preference, second_preference, third_preference    
    