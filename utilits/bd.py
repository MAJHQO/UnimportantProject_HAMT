import logging, database_simple as db

logger_bd=logging.getLogger("database")
logger_bd.setLevel(logging.INFO)

db_object=db.Database(False, database='AdminInfo')
    
def insertPC_Equipment(data:tuple):
    try:

        db_object.cursor.execute(f"""Insert into Equipment(Name,IP_Address,MAC_Address, Network_Name,CPU_Model, CPU_Frequency,RAM,HDD,Equipment_Category,Serial_Number,Invetory_Number,Equipment_Status,Cabinet_Number) values('Компьютер №{data[0]}','{data[5]}','{data[6]}','{data[7]}','{data[8]}','{data[9]}',{data[10] if str(data[10])!='nan' else 0},{data[11] if str(data[11])!='nan' else 0},'ПК','-','{data[4]}','-','{data[2]}')""")

        db_object.__connect__.commit()

    except Exception as ex:

        logger_bd.exception(f"Request execute was failed. Reason: {ex}")
        return False

def insertMonitor_Equipmet(data:tuple):
    try:

        db_object.cursor.execute(f"""Insert into Equipment(
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

        db_object.__connect__.commit()

    except Exception as ex:

        logger_bd.exception(f"Request execute was failed. Reason: {ex}")
        return False

def insertPrinter_Equipment(data:tuple):
    try:

        db_object.cursor.execute(f"""Insert into Equipment(
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

        db_object.__connect__.commit()

    except Exception as ex:

        logger_bd.exception(f"Request execute was failed. Reason: {ex}")
        return False

def insertProjector_Equipment(data:tuple):
    try:

        db_object.cursor.execute(f"""Insert into Equipment(
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

        db_object.__connect__.commit()

    except Exception as ex:

        logger_bd.exception(f"Request execute was failed. Reason: {ex}")
        return False
    
def insertScanner_Equipment(data:tuple):
    try:

        db_object.cursor.execute(f"""Insert into Equipment(
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
                                 '-'
                                 '{data[2]}')""")

        db_object.__connect__.commit()

    except Exception as ex:

        logger_bd.exception(f"Request execute was failed. Reason: {ex}")
        return False
    
def insertOther_Equipment(data:tuple):
    try:

        db_object.cursor.execute(f"""Insert into Equipment(
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

        db_object.__connect__.commit()

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

# db_object.create_table('Cabinets', {'ID':'INTEGER','Number': 'VARCHAR PRIMARY KEY'},700)
# db_object.create_table('Equipment_Status', {'ID':'INTEGER','Status_Name': 'VARCHAR PRIMARY KEY'},700)
# db_object.create_table('Equipment_Category', {'ID':'INTEGER','Category_Name': 'VARCHAR PRIMARY KEY'},700)
# db_object.create_table('Repair_Request', 
#                        {
#                         'ID':'INTEGER',
#                         'Request_Number': 'INT PRIMARY KEY',
#                         'TG_ID':'INTEGER', 
#                         'TG_Username':'VARCHAR',
#                         'Cabinet_Number':'VARCHAR REFERENCES Cabinets (Number)',
#                         'Request_Description':'VARCHAR',
#                         'Request_Status':'VARCHAR',},1300)
# db_object.create_table('Equipment', 
#                        {'ID':'INTEGER',
#                         'Name': 'VARCHAR PRIMARY KEY',
#                         'IP_Address':'VARCHAR', 
#                         'MAC_Address':'VARCHAR',
#                         'CPU_Model':'VARCHAR',
#                         'CPU_Frequency':'VARCHAR',
#                         'Network_Name': 'VARCHAR',
#                         'RAM':'INTEGER',
#                         'HDD':'INTEGER',
#                         'Equipment_Category':'VARCHAR REFERENCES Equipment_Category (Category_Name)',
#                         'Serial_Number':'VARCHAR',
#                         'Invetory_Number':'VARCHAR',
#                         'Equipment_Status':'VARCHAR REFERENCES Equipment_Status (Status_Name)',
#                         'Cabinet_Number':'VARCHAR REFERENCES Cabinets (Number)',},1300)
# db_object.create_table('Administrators', {
#     'ID':'INTEGER',
#     'FSL': 'VARCHAR',
#     'Login':'VARCHAR PRIMARY KEY',
#     'Mac_Address':'VARCHAR',
#     'Password':'VARCHAR',
#     'TG_Username':'VARCHAR',},1300)
# db_object.create_table('Users', {
#     'ID':'INTEGER',
#     'TG_ID': 'VARCHAR',
#     'Username':'VARCHAR',
#     'FSL':'VARCHAR'},1300)