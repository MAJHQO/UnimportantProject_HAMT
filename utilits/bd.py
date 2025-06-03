import logging, database_simple as db

logger_bd=logging.getLogger("database")
logger_bd.setLevel(logging.INFO)

db_object=db.Database(True, database='AdminInfo', user='postgres', password='5525', port='5890', host='localhost')
    
def insertPC_Equipment(data:tuple):
    try:

        db_object.request_execute(f"""Insert into Equipment(
                                 Name,
                                 IP_Address,
                                 MAC_Address,
                                 Network_Name,
                                 CPU_Model,
                                 CPU_Frequency,
                                 RAM,
                                 HDD,
                                 Equipment_Category,
                                 Serial_Number,
                                 Invetory_Number,
                                 Equipment_Status,
                                 Cabinet_Number) values('Компьютер №{data[0]}','{data[5]}','{data[6]}','{data[7]}','{data[8]}','{data[9]}',{data[10] if str(data[10])!='nan' else 0},{data[11] if str(data[11])!='nan' else 0},'ПК','-','{data[4]}','-','{data[2]}')""")

    except Exception as ex:

        logger_bd.exception(f"Request execute was failed. Reason: {ex}")
        return False

def insertMonitor_Equipmet(data:tuple):
    try:

        db_object.request_execute(f"""Insert into Equipment(
                                 Name,
                                 IP_Address,
                                 MAC_Address,
                                 Network_Name,
                                 CPU_Model,
                                 CPU_Frequency,
                                 RAM,
                                 HDD,
                                 Equipment_Category,
                                 Serial_Number,
                                 Invetory_Number,
                                 Equipment_Status,
                                 Cabinet_Number) values(
                                 'Монитор {str(data[0])+" "+data[12] if (len(data[12])!=0) else data[0]}',
                                 '-',
                                 '-',
                                 '-',
                                 '-',
                                 '-',
                                 0,
                                 0,
                                 'Монитор',
                                 '-',
                                 '{data[13]}',
                                 '-',
                                 '{data[2]}')""")

    except Exception as ex:

        logger_bd.exception(f"Request execute was failed. Reason: {ex}")
        return False

def insertPrinter_Equipment(data:tuple):
    try:

        db_object.request_execute(f"""Insert into Equipment(
                                 Name,
                                 IP_Address,
                                 MAC_Address,
                                 Network_Name,
                                 CPU_Model,
                                 CPU_Frequency,
                                 RAM,
                                 HDD,
                                 Equipment_Category,
                                 Serial_Number,
                                 Invetory_Number,
                                 Equipment_Status,
                                 Cabinet_Number) values(
                                 'Принтер {data[0]} {data[14]}',
                                 '-',
                                 '-',
                                 '-',
                                 '-',
                                 '-',
                                 0,
                                 0,
                                 'Принтер',
                                 '-',
                                 '-',
                                 '-',
                                 '{data[2]}')""")

    except Exception as ex:

        logger_bd.exception(f"Request execute was failed. Reason: {ex}")
        return False

def insertProjector_Equipment(data:tuple):
    try:

        db_object.request_execute(f"""Insert into Equipment(
                                 Name,
                                 IP_Address,
                                 MAC_Address,
                                 Network_Name,
                                 CPU_Model,
                                 CPU_Frequency,
                                 RAM,
                                 HDD,
                                 Equipment_Category,
                                 Serial_Number,
                                 Invetory_Number,
                                 Equipment_Status,
                                 Cabinet_Number) values(
                                 'Проектор №{data[0]}',
                                 '-',
                                 '-',
                                 '-',
                                 '-',
                                 '-',
                                 0,
                                 0,
                                 'Проектор',
                                 '-',
                                 '-',
                                 '-',
                                 '{data[2]}')""")

    except Exception as ex:

        logger_bd.exception(f"Request execute was failed. Reason: {ex}")
        return False
    
def insertScanner_Equipment(data:tuple):
    try:

        db_object.request_execute(f"""Insert into Equipment(
                                 Name,
                                 IP_Address,
                                 MAC_Address,
                                 Network_Name,
                                 CPU_Model,
                                 CPU_Frequency,
                                 RAM,
                                 HDD,
                                 Equipment_Category,
                                 Serial_Number,
                                 Invetory_Number,
                                 Equipment_Status,
                                 Cabinet_Number) values(
                                 'Сканер №{data[0]}',
                                 '-',
                                 '-',
                                 '-',
                                 '-',
                                 '-',
                                 0,
                                 0,
                                 'Сканер',
                                 '-',
                                 '-',
                                 '-',
                                 '{data[2]}')""")

    except Exception as ex:

        logger_bd.exception(f"Request execute was failed. Reason: {ex}")
        return False
    
def insertOther_Equipment(data:tuple):
    try:

        db_object.request_execute(f"""Insert into Equipment(
                                 Name,
                                 IP_Address,
                                 MAC_Address,
                                 Network_Name,
                                 CPU_Model,
                                 CPU_Frequency,
                                 RAM,
                                 HDD,
                                 Equipment_Category,
                                 Serial_Number,
                                 Invetory_Number,
                                 Equipment_Status,
                                 Cabinet_Number) values(
                                 '{data[17]}',
                                 '-',
                                 '-',
                                 '-',
                                 '-',
                                 '-',
                                 0,
                                 0,
                                 'Дополнительное оборудование',
                                 '-',
                                 '-',
                                 '-',
                                 '{data[2]}')""")

    except Exception as ex:

        logger_bd.exception(f"Request execute was failed. Reason: {ex}")
        return False

# db_object.delete_table("Repair_Request")
# db_object.delete_table("Equipment")
# db_object.delete_table("Administrators")
# db_object.delete_table("Cabinets")
# db_object.delete_table("Equipment_Status")
# db_object.delete_table("Equipment_Category")
# db_object.delete_table("Users")

# db_object.request_execute("CREATE SEQUENCE cab_seq START 1 INCREMENT BY 1;")
# db_object.request_execute("CREATE SEQUENCE eqStat_seq START 1 INCREMENT BY 1;")
# db_object.request_execute("CREATE SEQUENCE eqCat_seq START 1 INCREMENT BY 1;")
# db_object.request_execute("CREATE SEQUENCE req_seq START 1 INCREMENT BY 1;")
# db_object.request_execute("CREATE SEQUENCE equ_seq START 1 INCREMENT BY 1;")
# db_object.request_execute("CREATE SEQUENCE adm_seq START 1 INCREMENT BY 1;")
# db_object.request_execute("CREATE SEQUENCE usr_seq START 1 INCREMENT BY 1;")

# db_object.create_table('Cabinets', {'ID':"INTEGER NOT NULL DEFAULT nextval('cab_seq')",'Number': 'TEXT PRIMARY KEY'},780)
# db_object.create_table('Equipment_Status', {'ID':"INTEGER NOT NULL DEFAULT nextval('eqStat_seq')",'Status_Name': 'TEXT PRIMARY KEY'},740)
# db_object.create_table('Equipment_Category', {'ID':"INTEGER NOT NULL DEFAULT nextval('eqCat_seq')",'Category_Name': 'TEXT PRIMARY KEY'},740)
# db_object.create_table('Repair_Request', 
#                        {
#                         'ID':"INTEGER NOT NULL DEFAULT nextval('req_seq')",
#                         'Request_Number': 'INT PRIMARY KEY',
#                         'TG_ID':'INTEGER', 
#                         'TG_Username':'TEXT',
#                         'Cabinet_Number':'TEXT REFERENCES Cabinets (Number) ON DELETE CASCADE',
#                         'Request_Description':'TEXT',
#                         'Request_Status':'TEXT',},1300)
# db_object.create_table('Equipment', 
#                        {'ID':"INTEGER NOT NULL DEFAULT nextval('equ_seq')",
#                         'Name': 'TEXT PRIMARY KEY',
#                         'IP_Address':'TEXT', 
#                         'MAC_Address':'TEXT',
#                         'CPU_Model':'TEXT',
#                         'CPU_Frequency':'TEXT',
#                         'Network_Name': 'TEXT',
#                         'RAM':'INTEGER',
#                         'HDD':'INTEGER',
#                         'Equipment_Category':'TEXT REFERENCES Equipment_Category (Category_Name) ON DELETE CASCADE',
#                         'Serial_Number':'TEXT',
#                         'Invetory_Number':'TEXT',
#                         'Equipment_Status':'TEXT REFERENCES Equipment_Status (Status_Name) ON DELETE CASCADE',
#                         'Cabinet_Number':'TEXT REFERENCES Cabinets (Number) ON DELETE CASCADE',},4000)
# db_object.create_table('Administrators', {
#     'ID':"INTEGER NOT NULL DEFAULT nextval('adm_seq')",
#     'FSL': 'TEXT',
#     'Login':'TEXT PRIMARY KEY',
#     'Mac_Address':'TEXT',
#     'Password':'TEXT',
#     'TG_Username':'TEXT',},1300)
# db_object.create_table('Users', {
#     'ID':"INTEGER NOT NULL DEFAULT nextval('usr_seq')",
#     'TG_ID': 'TEXT',
#     'Username':'TEXT',
#     'FSL':'TEXT'},1300)