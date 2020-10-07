from py2neo import *

def connect_to_neo4j_db(password):
    db = Graph(password=password)
    return db

def client_exists(db,clientName):
    command = "MATCH (client:Client {name:'%(name)s'}) return client" %{"name":clientName}
    query= db.run(command)    
    
    if(str(query)==""):
        print("[x][store] Client node name: {} , does not exist".format(clientName))
        return False
    else:
        print("[*][store] Client node name: {} , exist".format(clientName))
        return True
    
def create_client_node(db,clientName): 
    command = "CREATE (client:Client {name:'%(name)s'} )" %{"name":clientName}
    db.run(command)
    print("[*][store] Client node name: {} , was created".format(clientName))
    
def banking_service_exists(db,clientName,bankingService):
    command = "MATCH (s:BankingService {name:'%(bankingService)s', client:'%(name)s' }) return s" %{"bankingService": bankingService,
                                                                                                    "name":clientName}   
    query= db.run(command)       
    if(str(query)==""):
        print("[x][store] BankingService node name: {} , does not exist".format(bankingService))
        return False
    else:
        print("[*][store] BankingService node name: {} ,exist".format(bankingService))
        return True
    
def create_banking_service(db,clientName,bankingService):
    command = "CREATE (bs:BankingService {name:'%(bankingService)s', client:'%(name)s', importance: 0} )" %{"name":clientName,
                                                                                                  "bankingService":bankingService}
    db.run(command)
    print("[*][store] BankingService node name: {} , was created".format(bankingService))
    
def create_client_banking_relationship(db,clientName,bankingService):
    command = """MATCH (c:Client {name:'%(clientName)s'})
MATCH (b:BankingService {name:'%(bankingService)s', client:'%(clientName)s'})
CREATE (c)-[:USE{graph_weight:[0]}]->(b)
""" %{"clientName":clientName, "bankingService":bankingService}
    db.run(command)
    print("[*][store] Relationship ({})-USE->({}) , was created".format(clientName,bankingService))
    
def add_importance_banking_service(db,clientName,bankingService):
    command_read = "MERGE (bs:BankingService {name: '%(bankingService)s', client:'%(name)s'}) return bs" %{"bankingService":bankingService,
                                                                                                                    "name":clientName}
    query=db.run(command_read)
    results = [record for record in query.data()]
    importance = int(results[0]['bs'].get("importance"))
    importance = str(importance + 1)
    
    command_write = "MERGE (bs:BankingService {name: '%(bankingService)s', client:'%(name)s'}) SET bs.importance = %(importance)s" %{
                                                                                                            "bankingService":bankingService,
                                                                                                            "name":clientName,
                                                                                                            "importance":importance}
    db.run(command_write)
    print("[*][store] Importance is {} in {}'s {} ".format(importance,clientName,bankingService))
    
def more_important_banking_services(db, clientName):
    command = "MATCH (bs:BankingService{client:'%(name)s'}) RETURN bs ORDER BY bs.importance DESC" %{"name": clientName}
    query=db.run(command)
    results = [record for record in query.data()]
    preferences = []
        
    for i in range(len(results)):
        preferences.append(str(results[i]['bs'].get("name")))
    
    return preferences

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
