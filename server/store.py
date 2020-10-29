from py2neo import *

def connect_to_neo4j_db(password):
    db = Graph(password=password)
    return db

def client_exists(db,clientId):
    command = "MATCH (client:Client {name:'%(name)s'}) return client" %{"name":clientId}
    query= db.run(command)    
    
    if(str(query)==""):
        print("[x][store] Client node name: {} , does not exist".format(clientId))
        return False
    else:
        print("[*][store] Client node name: {} , exist".format(clientId))
        return True
    
def create_client_node(db,clientId): 
    command = "CREATE (client:Client {name:'%(name)s'} )" %{"name":clientId}
    db.run(command)
    print("[*][store] Client node name: {} , was created".format(clientId))
    
def banking_service_exists(db,clientId,bankingService):
    command = "MATCH (s:BankingService {name:'%(bankingService)s', client:'%(name)s' }) return s" %{"bankingService": bankingService,
                                                                                                    "name":clientId}   
    query= db.run(command)       
    if(str(query)==""):
        print("[x][store] BankingService node name: {} , does not exist".format(bankingService))
        return False
    else:
        print("[*][store] BankingService node name: {} ,exist".format(bankingService))
        return True
    
def create_banking_service(db,clientId,bankingService):
    command = "CREATE (bs:BankingService {name:'%(bankingService)s', client:'%(name)s', importance: 0} )" %{"name":clientId,
                                                                                                  "bankingService":bankingService}
    db.run(command)
    print("[*][store] BankingService node name: {} , was created".format(bankingService))
    
def create_client_banking_relationship(db,clientId,bankingService):
    command = """MATCH (c:Client {name:'%(clientName)s'})
MATCH (b:BankingService {name:'%(bankingService)s', client:'%(clientName)s'})
CREATE (c)-[:USE{graph_weight:[0]}]->(b)
""" %{"clientName":clientId, "bankingService":bankingService}
    db.run(command)
    print("[*][store] Relationship ({})-USE->({}) , was created"
          .format(clientId,bankingService))
    
def add_importance_banking_service(db,clientId,bankingService):
    command_read = "MERGE (bs:BankingService {name: '%(bankingService)s', client:'%(name)s'}) return bs" %{"bankingService":bankingService,
                                                                                                                    "name":clientId}
    query=db.run(command_read)
    results = [record for record in query.data()]
    importance = int(results[0]['bs'].get("importance"))
    importance = str(importance + 1)
    
    command_write = "MERGE (bs:BankingService {name: '%(bankingService)s', client:'%(name)s'}) SET bs.importance = %(importance)s" %{
                                                                                                            "bankingService":bankingService,
                                                                                                            "name":clientId,
                                                                                                            "importance":importance}
    db.run(command_write)
    print("[*][store] Importance is {} in {}'s {} ".format(importance,clientId,bankingService))
    
def more_important_banking_services(db, clientId):
    command = "MATCH (bs:BankingService{client:'%(name)s'}) RETURN bs ORDER BY bs.importance DESC" %{"name": clientId}
    query=db.run(command)
    results = [record for record in query.data()]
    preferences = []
        
    for i in range(len(results)):
        preferences.append(str(results[i]['bs'].get("name")))
    
    return preferences

def create_loan(db,
                clientId,
                bankingService,
                loanNumber,
                participationNumber,
                paymentDate,
                paymentType,
                accountType,
                accountNumber,
                PaymentValue,
                depositTransactionCode,
                transactionDescriptionInDeposits,
                transactionTrackingNumber):
    
    command_create_loan = ("CREATE (l:Loan"
                           "{name:%(loanNumber)s,"
                           " client:'%(clientId)s',"
                           " bankingService:'%(bankingService)s',"
                           " participationNumber:%(participationNumber)s,"
                           " paymentDate:'%(paymentDate)s',"
                           " paymentType:'%(paymentType)s',"
                           " accountType:'%(accountType)s',"
                           " accountNumber:%(accountNumber)s,"
                           " PaymentValue:%(PaymentValue)s,"
                           " depositTransactionCode:%(depositTransactionCode)s,"
                           " transactionDescriptionInDeposits:'%(transactionDescriptionInDeposits)s',"
                           " transactionTrackingNumber:'%(transactionTrackingNumber)s'} )"
                           %{"clientId":clientId,
                             "loanNumber":loanNumber,
                             "bankingService":bankingService,
                             "participationNumber":participationNumber,
                             "paymentDate":paymentDate,
                             "paymentType":paymentType,
                             "accountType":accountType,
                             "accountNumber":accountNumber,
                             "PaymentValue":PaymentValue,
                             "depositTransactionCode":depositTransactionCode,
                             "transactionDescriptionInDeposits":transactionDescriptionInDeposits,
                             "transactionTrackingNumber":transactionTrackingNumber})
    db.run(command_create_loan)
    
    command_create_loan_relationship = """MATCH (l:Loan {name:%(loanNumber)s, client:'%(clientId)s'})
MATCH (b:BankingService {name:'%(bankingService)s', client:'%(clientId)s'})
CREATE (b)-[:DID{graph_weight:[0]}]->(l)
""" %{"loanNumber":loanNumber, 
    "clientId":clientId,
    "bankingService":bankingService}
    db.run(command_create_loan_relationship)
    
    print("[*][store] Loan , was created")
    
def create_transfer(db,
                clientId,
                bankingService,
                transferNumber,
                participationNumber,
                paymentDate,
                paymentType,
                accountType,
                accountNumber,
                PaymentValue,
                destinationAccount,
                transactionDescriptionInDeposits,
                transactionTrackingNumber):
    
    command_create_transfer = ("CREATE (t:Transfer"
                           "{name:%(transferNumber)s,"
                           " client:'%(clientId)s',"
                           " bankingService:'%(bankingService)s',"
                           " participationNumber:%(participationNumber)s,"
                           " paymentDate:'%(paymentDate)s',"
                           " paymentType:'%(paymentType)s',"
                           " accountType:'%(accountType)s',"
                           " accountNumber:%(accountNumber)s,"
                           " PaymentValue:%(PaymentValue)s,"
                           " destinationAccount:%(destinationAccount)s,"
                           " transactionDescriptionInDeposits:'%(transactionDescriptionInDeposits)s',"
                           " transactionTrackingNumber:'%(transactionTrackingNumber)s'} )"
                           %{"clientId":clientId,
                             "transferNumber":transferNumber,
                             "bankingService":bankingService,
                             "participationNumber":participationNumber,
                             "paymentDate":paymentDate,
                             "paymentType":paymentType,
                             "accountType":accountType,
                             "accountNumber":accountNumber,
                             "PaymentValue":PaymentValue,
                             "destinationAccount":destinationAccount,
                             "transactionDescriptionInDeposits":transactionDescriptionInDeposits,
                             "transactionTrackingNumber":transactionTrackingNumber})
    db.run(command_create_transfer)
    
    command_create_transfer_relationship = """MATCH (t:Transfer {name:%(transferNumber)s, client:'%(clientId)s'})
MATCH (b:BankingService {name:'%(bankingService)s', client:'%(clientId)s'})
CREATE (b)-[:DID{graph_weight:[0]}]->(t)
""" %{"transferNumber":transferNumber, 
    "clientId":clientId,
    "bankingService":bankingService}
    db.run(command_create_transfer_relationship)
    
    print("[*][store] Transfer , was created")


    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
