import flet as ft,time,datetime, requests,logging,os
from utilits import bd
from utilits.bd import db_object
import pandas as pd, string,random

from hashlib import sha384

ui_colors=['#E1DCE0',"#589A74"]
login_coLabelText=[
    'Привет! С возращением, что-то мы тебя потеряли.\nМного работы?',
    'Привет. С возращением!',
    'Вот ты и тут - поздравляем!']


logger_deskU=logging.getLogger("pages")
logger_deskU.setLevel(logging.INFO)

def password_generator(self):
    length=random.randint(10,25)

    lowercase_letters = list(string.ascii_lowercase)
    uppercase_letters = list(string.ascii_uppercase) 
    digits = list(string.digits)  
    special_characters = list(string.punctuation)
    
    password=""
    for i in range(0, length):
        a=random.randint(1,length)
        if(a%2==0 and a>7):
            if(a>7):
                password+=lowercase_letters[random.randint(0,len(digits)-1)]
            else:
                password+=lowercase_letters[a]
        elif(a>=5 and a%5==0):
            if (a%7==0):
                password+=uppercase_letters[a]
            else:
                password+=special_characters[a]
        elif(a>=3 or a%4==0):
            if(a%6==0):
                password+=special_characters[random.randint(0,len(digits)-1)]
            else:
                password+=digits[random.randint(0,len(digits)-1)]
        else:
            password+=uppercase_letters[a]
    self.page.controls[6].controls[1].value=password
    self.page.update()

def checkFieldOnIncosist(self:list,fieldType:int):
    """
    fieldType:
        0 - Start field check
    """

    if (fieldType==0):

        for control in self.page.controls:

            if(type(control)==ft.TextField and control.value==""):
                control.border_color=ft.Colors.RED_300

            elif (type(control)==ft.TextField and control.value!="" and control.hint_text=='Имя пользователя' and control.value.find("@")!=-1):
                control.border_color=ft.Colors.RED_300

            elif (type(control)==ft.TextField and control.value!="" and control.hint_text=='ФИО администратора' and len(control.value.split(" "))!=3):
                control.border_color=ft.Colors.RED_300

        self.page.update()

    elif (fieldType==1):

        chc=True

        for i in range(1,len(self.page.controls)):
            print(type(self.page.controls[i]))
            if (type(self.page.controls[i]) not in [ft.Row,ft.Column]):
                if((self.page.controls[i].value=="" or self.page.controls[i].value==None)):
                    chc=False

        self.page.update()

        return chc

def errorField(self):

    baseColor=None
    for control in self.page.controls:
        if (type(control) in [ft.TextField,ft.DropdownM2]):
            baseColor=control.border_color
            break

    for control in self.page.controls:

        if(type(control) in [ft.TextField,ft.DropdownM2]):
            control.border_color=ft.Colors.RED_300

    self.page.update()
    time.sleep(0.7)
    
    for control in self.page.controls:
        if (type(control) in [ft.TextField,ft.DropdownM2]):
            control.border_color=baseColor

    self.page.update()

def errorIcon(icon_obj: object, page:ft.Page):

    baseColor=icon_obj.icon_color

    icon_obj.icon_color=ft.Colors.RED
    page.update()
    time.sleep(0.7)
    icon_obj.icon_color=baseColor
    page.update()

def errorDialog(page:ft.Page,text:str):
    dialog=ft.AlertDialog(title="Ошибка при выполнении", content=ft.Text(text, size=13,font_family="Moderustic Light"))
    page.open(dialog)

def successField(self):

    for control in self.page.controls:

        if(type(control) in [ft.TextField,ft.DropdownM2]):
            control.border_color=ft.Colors.GREEN

    self.page.update()
    time.sleep(0.7)
    
    for control in self.page.controls:
        if (type(control) in [ft.TextField,ft.DropdownM2]):
            control.border_color=ft.Colors.BLACK

    self.page.update()

def contentColor_focus(self):
    self.control.border_color=ui_colors[1]
    self.page.update()

def contentColor_blur(self):
    self.control.border_color=ui_colors[0]
    self.page.update()

def pageClose(self):
    if (self.data=='close'):
        if(os.path.isfile("Desktop/Admin Configure")==True):
            try:
                lines=[]
                with open("Desktop/Admin Configure", 'r') as file:
                    lines=file.readlines()

                lines[0]=f"Enter Today:{datetime.datetime.now().strftime('%D')}"

                with open("Desktop/Admin Configure", 'w+') as file:
                    file.writelines(lines)

            except Exception as ex:

                logger_deskU.exception(f" {ex}")
                raise Exception(f" {ex}")

        self.page.window.destroy()

def searchInTable(self):
    actualTable=self.control.data[1].getTable(self.control.data[0]).controls[0].controls[0]
    if (self.control.value!=""):
        check=False
        columnArr:list=actualTable.columns
        width:int=actualTable.width
        searchTable:ft.DataTable=ft.DataTable(columns=columnArr, rows=[],width=width)

        for row in actualTable.rows:
            for cell in row.cells:
                if (cell.content.value.find(self.control.value)!=-1):
                    check=True
            if (check==True):
                searchTable.rows.append(row)
            check=False

        if (len(searchTable.rows)!=0):

            self.page.controls[2].controls.pop(0)
            self.page.controls[2].controls.append(searchTable)

    else:
        self.page.controls[2].controls.pop(0)
        self.page.controls[2].controls.append(actualTable)

    self.page.update()

def insert_equipment(row):
    try:
        result=None
        bd.insertPC_Equipment(row)
        if (type(row[12])==str):
            result=bd.insertMonitor_Equipmet(row)
        if(type(row[14])==str):
            result=bd.insertPrinter_Equipment(row)
        if (type(row[15])==str):
            result=bd.insertProjector_Equipment(row)
        if (type(row[16])==str):
            result=bd.insertScanner_Equipment(row)
        if (type(row[17])==str):
            result=bd.insertOther_Equipment(row)
        return result
    except Exception as ex:
        logger_deskU.exception(f" {ex}")
        raise Exception(f" {ex}")

def loadExcel(page:ft.Page,pd_obj):
    try:
        result=bd.reqExecute("Select Invetory_Number,Name from Equipment")
        if (result!=False and len(result)!=0):
            chc:bool=True
            chc_2:bool=None

            for row in pd_obj.values:
                if (type(row[0])==int):
                    for item in result:
                        chc=True
                        if (item[0]!="-"):
                            if(item[0]==row[4] or item[1]==f"Компьютер №{row[0]}"):
                                chc=False
                                break
                        elif (item[1] in [f"Монитор №{row[0]}", f"Принтер {row[0]} {row[14]}",f"Проектор №{row[0]}",f"Сканер №{row[0]}", row[17]]):
                            chc=False
                            break
                        
                    if (chc==True):
                        if(insert_equipment(row)==False):
                            chc_2=False         
                    if(chc_2==False):
                        errorDialog(page, "В момент экспорта данных из таблицы произошла ошибка")

        elif (len(result)==0):
            chc:bool=None
            for row in pd_obj.values:
                if (type(row[0])==int):
                    if(insert_equipment()==False):
                        chc=False
            if(chc==False):
                errorDialog(page, "В момент экспорта данных из таблицы произошла ошибка")
        else:
            errorDialog(page, "В момент выборки данных произошла ошибка")
    except Exception as ex:
        logger_deskU.exception(f" {ex}")
        raise Exception(f" {ex}")
                    
        

# class Table:
#     def __init__(self, column_list:list[ft.Text]):
#         self.__column=column_list
#         self.__table=ft.Row([ft.Column([ft.DataTable(self.__column)], scroll=True, height=500)], scroll=True, expand=1)
        
#     def viewMode(self,argc):
#         if (type(argc.page.controls[1].controls[0])==ft.Row):
#             for i in argc.page.controls[1].controls[0].controls[0].rows:
#                 for cell in range(0,len(i.cells)):
#                     if (i.cells[cell].data=="0" and cell==0):
#                         continue
#                     i.cells[cell].content.on_click=self.viewData_mode
#                     i.cells[cell].content.read_only=False

#             argc.control.content=ft.Text("Изменение")
#             argc.control.on_click=self.editMode

#         argc.page.update()

#     def editMode(self,argc): 
        
#         if (type(argc.page.controls[1].controls[0])==ft.Row):
#             for i in argc.page.controls[1].controls[0].controls[0].rows:
#                 for cell in range(0,len(i.cells)):
#                     if (i.cells[cell].data=="0" and cell==0):
#                         continue
#                     i.cells[cell].content.on_click=self.changeCellData
#                     i.cells[cell].content.read_only=True

#             argc.control.content=ft.Text("Просмотр")
#             argc.control.on_click=self.viewMode

#         argc.page.update()
        
#     def getTable(self_main, table_type:int):

#         result=None
#         cellName_arr=[]
        
#         if (table_type==1):
#             result=bd.reqExecute("Select * from Equipment")
#             cellName_arr.extend(["Name","IP_Address","MAC_Address","Network_Name","CPU_Model","CPU_Frequency","RAM","HDD","Equipment_Category","Serial_Number", "Invetory_Number" ,"Equipment_Status","Cabinet_Number"])
#         elif (table_type==2):
#             result=bd.reqExecute("Select * from Cabinets")
#             cellName_arr.extend(["Number"])
#         elif (table_type==3):
#             result=bd.reqExecute("Select * from Equipment_Status")
#             cellName_arr.extend(["Status_Name"])
#         elif (table_type==4):
#             result=bd.reqExecute("Select * from Equipment_Category")
#             cellName_arr.extend(["Status_Name"])
#         elif (table_type==5):
#             result=bd.reqExecute("Select * from Administrators")
#             cellName_arr.extend(["FSL", "Login", "Mac-Address", "Password", "TG_Username"])
#         else:
#             result=bd.reqExecute("Select * from Repair_Request")
#             cellName_arr.extend(["TG_ID","TG_Username","Request_Number","Cabinet_Number", "Request_Description","Request_Status"])

#         if (len(result)==0):
#             return None

#         if (len(self_main.__table.controls[0].controls[0].rows)>=1):
#            self_main.__table.controls[0].controls[0].rows.clear()

#         for i in range(0,len(result)):

#             self_main.__table.controls[0].controls[0].rows.append(ft.DataRow([]))

#             for j in range(0,len(result[i])):

#                 if (table_type==1):
#                     if (j in [2,5,6]):
#                         self_main.__table.controls[0].controls[0].rows[i].cells.append(ft.DataCell(ft.TextField(str((result[i][j])), text_align=ft.TextAlign.CENTER, read_only=True ,width=400, border_color=ft.Colors.TRANSPARENT, data=f"{(result[i][j])}|{(result[i][0])}|{(result[i][3])}|{int(table_type)}|{cellName_arr[j]}|Dropdown|{j}", on_click=self_main.viewData_mode), data="1"))
#                     else:
#                         self_main.__table.controls[0].controls[0].rows[i].cells.append(ft.DataCell(ft.TextField(str((result[i][j])), text_align=ft.TextAlign.CENTER, read_only=True ,width=400, border_color=ft.Colors.TRANSPARENT, data=f"{(result[i][j])}|{(result[i][0])}|{(result[i][3])}|{int(table_type)}|{cellName_arr[j]}|TextField", on_click=self_main.viewData_mode), data="1"))

#                 elif (table_type==0):
#                     if(j==3 or j==5):
#                         self_main.__table.controls[0].controls[0].rows[i].cells.append(ft.DataCell(ft.TextField(str((result[i][j])), width=400 ,text_align=ft.TextAlign.CENTER, read_only=True , border_color=ft.Colors.TRANSPARENT,data=f"{(result[i][j])}|{(result[i][1])}|{(result[i][2])}|{int(table_type)}|{cellName_arr[j]}|Dropdown|{j}|{(result[i][0])}", on_click=self_main.viewData_mode), data="0"))
#                     elif(j==0):
#                         self_main.__table.controls[0].controls[0].rows[i].cells.append(ft.DataCell(ft.TextField(str((result[i][j])), width=400 ,text_align=ft.TextAlign.CENTER, read_only=True , border_color=ft.Colors.TRANSPARENT,data=f"{(result[i][j])}|{(result[i][1])}|{(result[i][2])}|{int(table_type)}|{cellName_arr[j]}|TextField|{(result[i][0])}"), data="0"))
#                     else:

#                         self_main.__table.controls[0].controls[0].rows[i].cells.append(ft.DataCell(ft.TextField(str((result[i][j])), width=400 ,text_align=ft.TextAlign.CENTER, read_only=True , border_color=ft.Colors.TRANSPARENT,data=f"{(result[i][j])}|{(result[i][1])}|{(result[i][2])}|{int(table_type)}|{cellName_arr[j]}|TextField|{(result[i][0])}", on_click=self_main.viewData_mode), data="0"))
#                 elif (table_type==5):
#                     self_main.__table.controls[0].controls[0].rows[i].cells.append(ft.DataCell(ft.TextField(str((result[i][j])), width=400 ,text_align=ft.TextAlign.CENTER, read_only=True , border_color=ft.Colors.TRANSPARENT,data=f"{(result[i][j])}|{result[i][4]}|None|{int(table_type)}|{cellName_arr[j]}|TextField", on_click=self_main.viewData_mode), data=str(table_type)))
#                 else:
#                     self_main.__table.controls[0].controls[0].rows[i].cells.append(ft.DataCell(ft.TextField(str((result[i][j])), width=400 ,text_align=ft.TextAlign.CENTER, read_only=True , border_color=ft.Colors.TRANSPARENT,data=f"{(result[i][j])}|None|None|{int(table_type)}|{cellName_arr[j]}|TextField", on_click=self_main.viewData_mode), data=str(table_type)))

#         return self_main.__table
        
#     def updateTable(self,argc, onEditMode:bool=False):
            
#             table=None

#             if (type(argc.control.data)!=list):
#                 table=self.getTable(int(argc.control.data.split('|')[3]))
#             else:
#                 table=self.getTable(argc.control.data[0])

#             if (table!=None):
#                 argc.page.controls.pop(1)
#                 argc.page.controls.insert(1, table)

#                 if (onEditMode!=False):
#                     self.editMode(argc)
                
#                 if (type(argc.control.data)!=list):
#                     argc.control.data=f"{argc.page.overlay[len(argc.page.overlay)-1].content.value}_{argc.page.overlay[len(argc.page.overlay)-1].content.value}_{argc.control.data.split('|')[2]}_{argc.control.data.split('|')[3]}_{argc.control.data.split('|')[4]}"

#                 argc.page.update()
            
#             else:
#                 return None
        
#     def __changeData(self,argc):

#             baseColor=argc.page.overlay[len(argc.page.overlay)-1].content.border_color

#             if(argc.page.overlay[len(argc.page.overlay)-1].content.value==argc.control.data.split('|')[0] or argc.page.overlay[len(argc.page.overlay)-1].content.value=="" or argc.page.overlay[len(argc.page.overlay)-1].content.value==" "):

#                 argc.page.overlay[len(argc.page.overlay)-1].content.border_color=ft.Colors.RED_300

#             else:
#                 chc=True
#                 req=None

#                 if (argc.control.data.split('|')[3]=='1'):
#                     if (len(bd.reqExecute(f"Select * from Equipment where {argc.control.data.split('|')[4]}='{(argc.page.overlay[len(argc.page.overlay)-1].content.value)}'"))==0):
#                         bd.reqExecute(f"Update Equipment set {argc.control.data.split('|')[4]}='{(argc.page.overlay[len(argc.page.overlay)-1].content.value)}' where Name='{(argc.control.data.split('|')[1])}' AND Serial_Number='{(argc.control.data.split('|')[2])}'")
#                     else:
#                         argc.page.overlay[len(argc.page.overlay)-1].content.border_color=ft.Colors.RED_300
#                         chc=False
#                 elif (argc.control.data.split('|')[3]=='0'):
#                     if (len(bd.reqExecute(f"Select * from Repair_Request where {argc.control.data.split('|')[4]}='{(argc.page.overlay[len(argc.page.overlay)-1].content.value)}'"))==0):
#                         bd.reqExecute(f"Update Repair_Request set {argc.control.data.split('|')[4]}='{(argc.page.overlay[len(argc.page.overlay)-1].content.value)}' where TG_ID='{(argc.control.data.split('|')[1])}' AND TG_Username='{(argc.control.data.split('|')[2])}'")
#                         if (argc.control.data.split("|")[7]!=None):
#                             req=requests.post("https://api.telegram.org/bot7527441182:AAEI1sSafhOnZ1oLgeRgdaJALzxoHEmiWLY/sendMessage", data={"chat_id": argc.control.data.split('|')[1], "text": f'Статус заявки №{argc.control.data.split("|")[7]} изменен на: {argc.page.overlay[len(argc.page.overlay)-1].content.value}'})
#                         else:
#                             req=requests.post("https://api.telegram.org/bot7527441182:AAEI1sSafhOnZ1oLgeRgdaJALzxoHEmiWLY/sendMessage", data={"chat_id": argc.control.data.split('|')[1], "text": f'Статус заявки №{argc.control.data.split("|")[6]} изменен на: {argc.page.overlay[len(argc.page.overlay)-1].content.value}'})
#                     else:
#                         argc.page.overlay[len(argc.page.overlay)-1].content.border_color=ft.Colors.RED_300
#                         chc=False
#                 else:
#                     if (argc.control.data.split('|')[3]=='2'):
#                         if (len(bd.reqExecute(f"Select * from Cabinets where {argc.control.data.split('|')[4]}='{(argc.page.overlay[len(argc.page.overlay)-1].content.value)}'"))==0):
#                             bd.reqExecute(f"Update Cabinets set {argc.control.data.split('|')[4]}='{(argc.page.overlay[len(argc.page.overlay)-1].content.value)}' where {argc.control.data.split('|')[4]}='{(argc.control.data.split('|')[0])}'")
#                         else:
#                             argc.page.overlay[len(argc.page.overlay)-1].content.border_color=ft.Colors.RED_300
#                             chc=False
#                     elif(argc.control.data.split('|')[3]=='3'):
#                         if (len(bd.reqExecute(f"Select * from Equipment_Status where {argc.control.data.split('|')[4]}='{(argc.page.overlay[len(argc.page.overlay)-1].content.value)}'"))==0):
#                             bd.reqExecute(f"Update Equipment_Status set {argc.control.data.split('|')[4]}='{(argc.page.overlay[len(argc.page.overlay)-1].content.value)}' where {argc.control.data.split('|')[4]}='{(argc.control.data.split('|')[0])}'")
#                         else:
#                             argc.page.overlay[len(argc.page.overlay)-1].content.border_color=ft.Colors.RED_300
#                             chc=False
#                     elif(argc.control.data.split('|')[3]=='4'):
#                         if (len(bd.reqExecute(f"Select * from Equipment_Category where {argc.control.data.split('|')[4]}='{(argc.page.overlay[len(argc.page.overlay)-1].content.value)}'"))==0):
#                             bd.reqExecute(f"Update Equipment_Category set {argc.control.data.split('|')[4]}='{(argc.page.overlay[len(argc.page.overlay)-1].content.value)}' where {argc.control.data.split('|')[4]}='{(argc.control.data.split('|')[0])}'")
#                         else:
#                             argc.page.overlay[len(argc.page.overlay)-1].content.border_color=ft.Colors.RED_300
#                             chc=False


#                 if(chc==True or req.status_code==200):
#                     self.updateTable(argc,True)
#                     argc.page.overlay[len(argc.page.overlay)-1].content.border_color=ft.Colors.GREEN

#             argc.page.update()

#             time.sleep(0.7)

#             argc.page.overlay[len(argc.page.overlay)-1].content.border_color=baseColor

#             argc.page.update()
        
#     def changeCellData(self,argc):

#         changeCellData_Dialog=ft.AlertDialog(actions=[
#                                                      ft.ElevatedButton("Изменить", on_click=self.__changeData, data=argc.control.data,width=100),
#                                                      ft.ElevatedButton("Выйти",width=80, on_click=lambda _: argc.page.close(changeCellData_Dialog))
#                                                  ], title=ft.Text("Изменение данных"))
        
#         if(argc.control.data.split('|')[5]=="Dropdown"):
#             result=None
#             if(argc.control.data.split('|')[3]=='1'):

#                 if (argc.control.data.split('|')[6]=='2'):
#                     result=bd.reqExecute("Select * from Equipment_Category")
#                 elif(argc.control.data.split('|')[6]=='5'):
#                     result=bd.reqExecute("Select * from Equipment_Status")
#                 elif(argc.control.data.split('|')[6]=='6'):
#                     result=bd.reqExecute("Select * from Cabinets")

#             elif (argc.control.data.split('|')[3]=='0'):

#                 if(argc.control.data.split('|')[6]=='3'):
#                     result=bd.reqExecute("Select * from Cabinets")
#                 else:
#                     result=bd.reqExecute("Select * from Repair_Request")

#             if (len(result)!=0):

#                 if(argc.control.data.split('|')[3]=='0' and argc.control.data.split('|')[6]!='3'):
#                     changeCellData_Dialog.content=ft.DropdownM2(value=argc.control.data.split('|')[0],options=[
#                         ft.dropdownm2.Option("Исполнено"),
#                         ft.dropdownm2.Option("В работе"),
#                         ft.dropdownm2.Option("Ожидание"),
#                         ft.dropdownm2.Option("Отказано в выполнении"),
#                     ], border_color=ft.Colors.TRANSPARENT)

#                 else:

#                     changeCellData_Dialog.content=ft.DropdownM2(value=argc.control.data.split('|')[0],options=[], border_color=ft.Colors.TRANSPARENT)

#                     for i in result:
#                         changeCellData_Dialog.content.options.append(ft.dropdownm2.Option(i[0]))

#             else:
#                 changeCellData_Dialog.content=ft.DropdownM2(' ',[], border_color=ft.Colors.TRANSPARENT)

#         else:
#             changeCellData_Dialog.content=ft.TextField(argc.control.data.split('|')[0])
     
#         argc.page.open(changeCellData_Dialog)

    
#     def viewData_mode(self,argc):
        
#         viewMode_dialog=ft.AlertDialog(title=ft.Text("Просмотр данных"),
#                                        content=ft.TextField(argc.control.data.split("|")[0],text_align=ft.TextAlign.CENTER,border_color=ft.Colors.TRANSPARENT,read_only=True,text_size=17, width=200 ,multiline=True), 
#                                        actions=[ft.ElevatedButton("Выйти",on_click=lambda _:argc.page.close(viewMode_dialog))],)

#         argc.page.open(viewMode_dialog)

    