import flet as ft,time,datetime, requests,logging,os,csv
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
        if(os.path.isfile(".\Admin Configure" if(self.page.platform==ft.PagePlatform.WINDOWS) else "./Admin Configure")==True):
            try:
                lines=[]
                with open(".\Admin Configure" if(self.page.platform==ft.PagePlatform.WINDOWS) else "./Admin Configure", 'r') as file:
                    lines=file.readlines()

                lines[0]=f"Enter Today:{datetime.datetime.now().strftime('%D')}"

                with open(".\Admin Configure" if(self.page.platform==ft.PagePlatform.WINDOWS) else "./Admin Configure", 'w+') as file:
                    file.writelines(lines)

            except Exception as ex:

                logger_deskU.exception(f" {ex}")
                raise Exception(f" {ex}")

        self.page.window.destroy()

def createFolder(path:str):
    try:
        os.mkdir(path)
        logger_deskU.exception(f"Папка по пути ['{path}'] создана успешно")
    except FileExistsError as ex:
        logger_deskU.exception(f"Пока по пути ['{path}'] уже существует")
        raise Exception(f" {ex}")
    except PermissionError as ex:
        logger_deskU.exception(f"Отказано в доступе: не удается создать папку ['{path}']")
        raise Exception(f" {ex}")
    except Exception as ex:
        logger_deskU.exception(f"Error: {ex}")
        raise Exception(f" {ex}")

def searchInTable(self):
    actualTable=self.control.data[1].getTable(db_object)
    actualTable=actualTable.controls[0].controls[0]
    if (self.control.value!=""):
        check=False
        columnArr:list=actualTable.columns
        width:int=actualTable.width
        searchTable:ft.DataTable=ft.DataTable(columns=columnArr, rows=[],width=width)

        for row in actualTable.rows:
            for cell in row.cells:
                if (type(cell.content)==ft.TextField):
                    if(cell.content.value.find(self.control.value)!=-1):
                        check=True
            if (check==True):
                searchTable.rows.append(row)
            check=False

        if (len(searchTable.rows)!=0):

            self.page.controls[1].controls[0].controls.pop(0)
            self.page.controls[1].controls[0].controls.append(searchTable)

    else:
        self.page.controls[1].controls[0].controls.pop(0)
        self.page.controls[1].controls[0].controls.append(actualTable)

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

def loadExcel(page:ft.Page,pd_obj, table_obj:object):
    try:
        result=db_object.request_execute("Select Invetory_Number,Name from Equipment")
        if (result!=False and len(result)!=0):
            chc:bool=True

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
                            errorDialog(page, "В момент экспорта данных из таблицы произошла ошибка")

        elif (len(result)==0):
            chc:bool=None
            for row in pd_obj.values:
                if (type(row[0])==int):
                    if(insert_equipment(row)==False):
                        chc=False
            if(chc==False):
                errorDialog(page, "В момент экспорта данных из таблицы произошла ошибка")
        else:
            errorDialog(page, "В момент выборки данных произошла ошибка")

        page_update(page,table_obj)
    except Exception as ex:
        logger_deskU.exception(f" {ex}")
        raise Exception(f" {ex}")
    
def page_update(page, table_obj:object):
    try:
        page.controls.pop(1)
        table=table_obj.getTable(db_object)
        page.controls.insert(1,table)
        page.update()
    except Exception as ex:
        raise Exception(ex)
    
def change_eqPage_Mode(page:ft.Page, table_obj:object):
    try:
        if (type(page.controls[1])==ft.Row and type(page.controls[1].controls[0].controls[0])==ft.DataTable):
            for rows in page.controls[1].controls[-1].controls[0].rows:
                for i in range(0,len(rows.cells)):
                    if(i!=6):
                        rows.cells[i].content.on_click=None

            page.update()
    except Exception as ex:
        raise Exception(ex)