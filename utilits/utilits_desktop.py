import flet as ft,time,datetime
from utilits import bd

ui_colors=['#E1DCE0',"#589A74"]
login_coLabelText=[
    'Привет! С возращением, что-то мы тебя потеряли.\nМного работы?',
    'Привет. С возращением!',
    'Вот ты и тут - поздравляем!']

def dynamicPassCheck(self, dynamicCheck=True):

    if (dynamicCheck==True):

        if (self.control.value==''):
            self.control.border_color=ft.colors.BLACK

        elif (len(self.control.value)<=15):

            self.control.border_color=ft.colors.RED_300

        else:

            passwordCheck=[0,0,0,0]
            elemSum=0

            for i in self.control.value:

                if (i>='A' and i<='Z'):
                    passwordCheck[0]+=1

                elif (i>='a' and i<='z'):
                    passwordCheck[1]+=1

                elif (i>='0' and i<='9'):
                    passwordCheck[2]+=1

                elif (i in ['%','$','@','*','&','<','>','#','!']):
                    passwordCheck[3]+=1

            for i in passwordCheck:
                elemSum+=int(i)

            if (elemSum>=1 and elemSum<=8):
                if((passwordCheck[0]>0 and passwordCheck[0]<=3) and (passwordCheck[1]>0 and passwordCheck[1]<=3) and (passwordCheck[2]>0 and passwordCheck[2]<=3) and (passwordCheck[3]>0 and passwordCheck[3]<=2)):
                    self.control.border_color=ft.colors.ORANGE_300 
                else:
                    self.control.border_color=ft.colors.RED_300 

            elif (elemSum>=9):
                if( passwordCheck[0]>=5 and passwordCheck[1]>3 and passwordCheck[2]>=4 and  passwordCheck[3]>2):
                    self.control.border_color=ft.colors.GREEN_300

                else:
                    self.control.border_color=ft.colors.ORANGE_300 
                    

        self.page.update()

    else:

        for control in self.page.controls:

            if (type(control)==ft.TextField and control.hint_text=='Пароль'):

                if (control.value==''):
                    return False
                elif (len(control.value)<=15):

                    return False

                else:

                    passwordCheck=[0,0,0,0]
                    elemSum=0

                    for i in control.value:

                        if (i>='A' and i<='Z'):
                            passwordCheck[0]+=1

                        elif (i>='a' and i<='z'):
                            passwordCheck[1]+=1

                        elif (i>='0' and i<='9'):
                            passwordCheck[2]+=1

                        elif (i in ['%','$','@','*','&','<','>','#','!']):
                            passwordCheck[3]+=1

                    for i in passwordCheck:
                        elemSum+=int(i)

                    if (elemSum>=1 and elemSum<=8):
                        if((passwordCheck[0]>0 and passwordCheck[0]<=3) and (passwordCheck[1]>0 and passwordCheck[1]<=3) and (passwordCheck[2]>0 and passwordCheck[2]<=3) and (passwordCheck[3]>0 and passwordCheck[3]<=2)):
                            return True
                        else:
                            return False

                    elif (elemSum>=9):
                        if( passwordCheck[0]>=5 and passwordCheck[1]>3 and passwordCheck[2]>=4 and  passwordCheck[3]>2):
                            return True
                
    return False

def checkFieldOnIncosist(self:list,fieldType:int):
    """
    fieldType:
        0 - Start field check
    """

    if (fieldType==0):

        for control in self.page.controls:

            if(type(control)==ft.TextField and control.value==""):
                control.border_color=ft.colors.RED_300

            elif (type(control)==ft.TextField and control.value!="" and control.hint_text=='Имя пользователя' and control.value.find("@")!=-1):
                control.border_color=ft.colors.RED_300

            elif (type(control)==ft.TextField and control.value!="" and control.hint_text=='ФИО администратора' and len(control.value.split(" "))!=3):
                control.border_color=ft.colors.RED_300

        self.page.update()

    elif (fieldType==1):

        chc=True

        for i in range(1,len(self.page.controls)):
            if (self.page.controls[i]=="" or self.page.controls[i]==None):
                self.page.controls[i].border_color=ft.colors.RED_300
                chc=False
            else:
                self.page.controls[i].border_color=ft.colors.GREEN

        self.page.update()

        return chc

def errorField(self):

    for control in self.page.controls:

        if(type(control)==ft.TextField):
            control.border_color=ft.colors.RED_300

    self.page.update()
    time.sleep(0.7)
    
    for control in self.page.controls:
        if (type(control)==ft.TextField):
            control.border_color=ft.colors.BLACK

    self.page.update()

def successField(self):

    for control in self.page.controls:

        if(type(control)==ft.TextField):
            control.border_color=ft.colors.GREEN

    self.page.update()
    time.sleep(0.7)
    
    for control in self.page.controls:
        if (type(control)==ft.TextField):
            control.border_color=ft.colors.BLACK

    self.page.update()

def contentColor_focus(self):
    self.control.border_color=ui_colors[1]
    self.page.update()

def contentColor_blur(self):
    self.control.border_color=ui_colors[0]
    self.page.update()

def pageClose(self):
    if (self.data=='close'):
        lines=[]
        with open("Admin Configure", 'r') as file:
            lines=file.readlines()

        lines[1]=f"Enter Today:{datetime.datetime.now().strftime("%D")}"

        with open("Admin Configure", 'w+') as file:
            file.writelines(lines)

        self.page.window.destroy()

class Table:
    def __init__(self, column_list:list[ft.Text],table_width:int):
        self.__column=column_list
        self.__table=ft.ListView([ft.Row([ft.DataTable(self.__column,width=table_width)], alignment=ft.MainAxisAlignment.CENTER , scroll=True)
            ], height=500)
        
    def viewMode(self,argc):

        for i in range(0,len(argc.page.controls[1].controls[0].controls[0].rows)):
            for cell in argc.page.controls[1].controls[0].controls[0].rows[i].cells:
                cell.content.on_click=None
                cell.content.read_only=False

        argc.control.content=ft.Text("Изменение")
        argc.control.on_click=self.editMode

        argc.page.update()

    def editMode(self,argc): 

        for i in range(0,len(argc.page.controls[1].controls[0].controls[0].rows)):
            for cell in argc.page.controls[1].controls[0].controls[0].rows[i].cells:
                cell.content.on_click=self.changeCellData
                cell.content.read_only=True

        argc.control.content=ft.Text("Просмотр")
        argc.control.on_click=self.viewMode

        argc.page.update()
        
    def getTable(self_main, table_type:bool):

        result=None
        cellName_arr=[]
        
        if (table_type==1):
            result=bd.reqExecute("Select * from Equipment")
            cellName_arr.extend(["Name","Components","Equipment_Category","Serial_Number", "Invetory_Number" ,"Equipment_Status","Cabinet_Number"])
        elif (table_type==2):
            result=bd.reqExecute("Select * from Cabinets")
            cellName_arr.extend(["Number"])
        elif (table_type==3):
            result=bd.reqExecute("Select * from Equipment_Status")
            cellName_arr.extend(["Status_Name"])
        elif (table_type==4):
            result=bd.reqExecute("Select * from Equipment_Category")
            cellName_arr.extend(["Status_Name"])
        else:
            result=bd.reqExecute("Select * from Repair_Request")
            cellName_arr.extend(["TG_ID","TG_Username","Request_Number","Cabinet_Number", "Request_Description","Request_Status"])

        if (len(result)==0):
            return None

        if (len(self_main.__table.controls[0].controls[0].rows)>1):
           self_main.__table.controls[0].controls[0].rows.clear()

        for i in range(0,len(result)):

            self_main.__table.controls[0].controls[0].rows.append(ft.DataRow([]))

            for j in range(0,len(result[i])):

                if (table_type==1):
                    if (j in [2,5,6]):
                        self_main.__table.controls[0].controls[0].rows[i].cells.append(ft.DataCell(ft.TextField(str(result[i][j]), text_align=ft.TextAlign.CENTER, read_only=True ,width=400, border_color=ft.colors.TRANSPARENT, data=f"{result[i][j]}|{result[i][0]}|{result[i][3]}|{int(table_type)}|{cellName_arr[j]}|Dropdown|{j}")))
                    else:
                        self_main.__table.controls[0].controls[0].rows[i].cells.append(ft.DataCell(ft.TextField(str(result[i][j]), text_align=ft.TextAlign.CENTER, read_only=True ,width=400, border_color=ft.colors.TRANSPARENT, data=f"{result[i][j]}|{result[i][0]}|{result[i][3]}|{int(table_type)}|{cellName_arr[j]}|TextField")))

                elif (table_type==0):
                    if(j==3 or j==5):
                        self_main.__table.controls[0].controls[0].rows[i].cells.append(ft.DataCell(ft.TextField(str(result[i][j]), width=400 ,text_align=ft.TextAlign.CENTER, read_only=True , border_color=ft.colors.TRANSPARENT,data=f"{result[i][j]}|{result[i][1]}|{result[i][2]}|{int(table_type)}|{cellName_arr[j]}|Dropdown|{j}")))
                    else:

                        self_main.__table.controls[0].controls[0].rows[i].cells.append(ft.DataCell(ft.TextField(str(result[i][j]), width=400 ,text_align=ft.TextAlign.CENTER, read_only=True , border_color=ft.colors.TRANSPARENT,data=f"{result[i][j]}|{result[i][1]}|{result[i][2]}|{int(table_type)}|{cellName_arr[j]}|TextField")))

                else:
                    self_main.__table.controls[0].controls[0].rows[i].cells.append(ft.DataCell(ft.TextField(str(result[i][j]), width=400 ,text_align=ft.TextAlign.CENTER, read_only=True , border_color=ft.colors.TRANSPARENT,data=f"{result[i][j]}|None|None|{int(table_type)}|{cellName_arr[j]}|TextField")))

        return self_main.__table
        
    def updateTable(self,argc):
            
            table=None

            if (type(argc.control.data)!=list):
                table=self.getTable(int(argc.control.data.split('|')[3]))
            else:
                table=self.getTable(argc.control.data[0])
            argc.page.controls.pop(1)
            argc.page.controls.insert(1, table)
            
            if (type(argc.control.data)!=list):
                argc.control.data=f"{argc.page.overlay[len(argc.page.overlay)-1].content.value}_{argc.page.overlay[len(argc.page.overlay)-1].content.value}_{argc.control.data.split('|')[2]}_{argc.control.data.split('|')[3]}_{argc.control.data.split('|')[4]}"

            argc.page.update()
        
    def __changeData(self,argc):

            if(argc.page.overlay[len(argc.page.overlay)-1].content.value==argc.control.data.split('|')[0] or argc.page.overlay[len(argc.page.overlay)-1].content.value=="" or argc.page.overlay[len(argc.page.overlay)-1].content.value==" "):

                argc.page.overlay[len(argc.page.overlay)-1].content.border_color=ft.colors.RED_300

            else:
                chc=True

                if (argc.control.data.split('|')[3]=='1'):
                    if (len(bd.reqExecute(f"Select * from Equipment where {argc.control.data.split('|')[4]}='{argc.page.overlay[len(argc.page.overlay)-1].content.value}'"))==0):
                        bd.reqExecute(f"Update Equipment set {argc.control.data.split('|')[4]}='{argc.page.overlay[len(argc.page.overlay)-1].content.value}' where Name='{argc.control.data.split('|')[1]}' AND Serial_Number='{argc.control.data.split('|')[2]}'")
                    else:
                        argc.page.overlay[len(argc.page.overlay)-1].content.border_color=ft.colors.RED_300
                        chc=False
                elif (argc.control.data.split('|')[3]=='0'):
                    if (len(bd.reqExecute(f"Select * from Repair_Request where {argc.control.data.split('|')[4]}='{argc.page.overlay[len(argc.page.overlay)-1].content.value}'"))==0):
                        bd.reqExecute(f"Update Repair_Request set {argc.control.data.split('|')[4]}='{argc.page.overlay[len(argc.page.overlay)-1].content.value}' where FSL='{argc.control.data.split('|')[1]}' AND TG_Username='{argc.control.data.split('|')[2]}'")
                    else:
                        argc.page.overlay[len(argc.page.overlay)-1].content.border_color=ft.colors.RED_300
                        chc=False
                else:
                    if (argc.control.data.split('|')[3]=='2'):
                        if (len(bd.reqExecute(f"Select * from Cabinets where {argc.control.data.split('|')[4]}='{argc.page.overlay[len(argc.page.overlay)-1].content.value}'"))==0):
                            bd.reqExecute(f"Update Cabinets set {argc.control.data.split('|')[4]}='{argc.page.overlay[len(argc.page.overlay)-1].content.value}' where {argc.control.data.split('|')[4]}='{argc.control.data.split('|')[0]}'")
                        else:
                            argc.page.overlay[len(argc.page.overlay)-1].content.border_color=ft.colors.RED_300
                            chc=False
                    elif(argc.control.data.split('|')[3]=='3'):
                        if (len(bd.reqExecute(f"Select * from Equipment_Status where {argc.control.data.split('|')[4]}='{argc.page.overlay[len(argc.page.overlay)-1].content.value}'"))==0):
                            bd.reqExecute(f"Update Equipment_Status set {argc.control.data.split('|')[4]}='{argc.page.overlay[len(argc.page.overlay)-1].content.value}' where {argc.control.data.split('|')[4]}='{argc.control.data.split('|')[0]}'")
                        else:
                            argc.page.overlay[len(argc.page.overlay)-1].content.border_color=ft.colors.RED_300
                            chc=False
                    elif(argc.control.data.split('|')[3]=='4'):
                        if (len(bd.reqExecute(f"Select * from Equipment_Category where {argc.control.data.split('|')[4]}='{argc.page.overlay[len(argc.page.overlay)-1].content.value}'"))==0):
                            bd.reqExecute(f"Update Equipment_Category set {argc.control.data.split('|')[4]}='{argc.page.overlay[len(argc.page.overlay)-1].content.value}' where {argc.control.data.split('|')[4]}='{argc.control.data.split('|')[0]}'")
                        else:
                            argc.page.overlay[len(argc.page.overlay)-1].content.border_color=ft.colors.RED_300
                            chc=False

                if(chc==True):
                    self.updateTable(argc)
                    argc.page.overlay[len(argc.page.overlay)-1].content.border_color=ft.colors.GREEN

            argc.page.update()

            time.sleep(0.7)

            argc.page.overlay[len(argc.page.overlay)-1].content.border_color=ft.colors.BLACK

            argc.page.update()
        
    def changeCellData(self,argc):

        changeCellData_Dialog=ft.AlertDialog(modal=True,
                                                 actions=[
                                                     ft.ElevatedButton("Изменить", on_click=self.__changeData, data=argc.control.data,width=100),
                                                     ft.ElevatedButton("Выйти",width=80, on_click=lambda _: argc.page.close(changeCellData_Dialog))
                                                 ], title=ft.Text("Изменение данных"))
        
        if(argc.control.data.split('|')[5]=="Dropdown"):
            result=None
            if(argc.control.data.split('|')[3]=='1'):

                if (argc.control.data.split('|')[6]=='2'):
                    result=bd.reqExecute("Select * from Equipment_Category")
                elif(argc.control.data.split('|')[6]=='5'):
                    result=bd.reqExecute("Select * from Equipment_Status")
                elif(argc.control.data.split('|')[6]=='6'):
                    result=bd.reqExecute("Select * from Cabinets")

            elif (argc.control.data.split('|')[3]=='0'):

                if(argc.control.data.split('|')[6]=='3'):
                    result=bd.reqExecute("Select * from Cabinets")
                else:
                    result=bd.reqExecute("Select * from Request_Status")

            if (len(result)!=0):

                changeCellData_Dialog.content=ft.DropdownM2(value=argc.control.data.split('|')[0],options=[], border_color=ft.colors.TRANSPARENT)

                for i in result:
                     changeCellData_Dialog.content.options.append(ft.dropdownm2.Option(i[0]))

            else:
                changeCellData_Dialog.content=ft.DropdownM2(' ',[], border_color=ft.colors.TRANSPARENT)

        else:
            changeCellData_Dialog.content=ft.TextField(argc.control.data.split('|')[0])
     
        argc.page.open(changeCellData_Dialog)
    