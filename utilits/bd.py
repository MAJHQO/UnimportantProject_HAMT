import psycopg2 as sq, logging,sys,os

logger_bd=logging.getLogger("database")
logger_bd.setLevel(logging.INFO)

connect=None

def connectionToDatabase():

    try:

        connnection=sq.connect(host="localhost",database="AdminInfo", user="postgres", password="5525", port='5890')
            
        logger_bd.info("Connected to database was successfull")

        return connnection

    except Exception as ex:
        
        logger_bd.error(f"Connection to database was failed. Reason: {ex}")
        raise Exception("Connection to database was failed")

connect=connectionToDatabase()

def reqExecute(request:str):

    try:

        cursor=connect.cursor()

        cursor.execute(request)

        connect.commit()

        if (request.startswith("Select")):

            result=cursor.fetchall()

            return result

    except Exception as ex:

        logger_bd.exception(f"Request execute was failed. Reason: {ex}")
        return False


# reqExecute("Drop table Repair_Request")
# reqExecute("Drop table Equipment")
# reqExecute("Drop table Administrators")
# reqExecute("Drop table Cabinets")
# reqExecute("Drop table Equipment_Status")
# reqExecute("Drop table Equipment_Category")
# reqExecute("Drop table Users")

# reqExecute("""Create table Cabinets(
#            Number VARCHAR PRIMARY KEY)""")

# reqExecute("""Create table Equipment_Status(
#            Status_Name VARCHAR PRIMARY KEY)""")

# reqExecute("""Create table Equipment_Category(
#            Category_Name VARCHAR PRIMARY KEY)""")

# reqExecute("""Create table Repair_Request(
#             Request_Number INT PRIMARY KEY,
#             TG_ID INTEGER,
#             TG_Username VARCHAR,
#             Cabinet_Number VARCHAR,
#             Request_Description VARCHAR,
#             Request_Status VARCHAR,
#             FOREIGN KEY (Cabinet_Number)  REFERENCES Cabinets (Number))""")

# reqExecute("""Create table Equipment(
#             Name VARCHAR PRIMARY KEY,
#             Components VARCHAR,
#             Equipment_Category VARCHAR,
#             Serial_Number VARCHAR,
#             Invetory_Number VARCHAR,
#             Equipment_Status VARCHAR,
#             Cabinet_Number VARCHAR,
#             FOREIGN KEY (Equipment_Category)  REFERENCES Equipment_Category (Category_Name),
#             FOREIGN KEY (Equipment_Status)  REFERENCES Equipment_Status (Status_Name),
#             FOREIGN KEY (Cabinet_Number)  REFERENCES Cabinets (Number))""")

# reqExecute("""Create table Administrators(
#             FSL VARCHAR,
#             Login VARCHAR PRIMARY KEY,
#             Mac_Address VARCHAR,
#             Password VARCHAR,
#             TG_Username VARCHAR);""")

# reqExecute("""Create table Users(
#            TG_ID INTEGER,
#            Username VARCHAR,
#            FSL VARCHAR)""")

#   Закрепление оборудования за преподователем || сотрудников техникума ?
#   Таблица категорий оборудования


#reqExecute("Insert into Equipment(Name, Components, Equipment_Category, Serial_Number, Equipment_Status, Cabinet_Number) values ('ПК-305', 'Intel i3-12800, 16GB 3200GHZ, 1TB SSD', 'Компьютер' ,2315123, 'Исправен', 305)")
#reqExecute("""""")