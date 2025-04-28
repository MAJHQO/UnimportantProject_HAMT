import flet as ft, time, hashlib as hLib, logging,datetime,requests,os
from utilits import bd,utilits_desktop as deskU
from random import randint

import uuid 

from cryptography.fernet import Fernet
from hashlib import sha384



logger_pages=logging.getLogger("pages")
logger_pages.setLevel(logging.INFO)



def addData_page(self_main):

    def clearFields(self):
        
        for i in range(1, len(self.page.controls)):
            self.page.controls[i].value=""

        self.page.update()

    def addData(self):

        if(self.control.data[0]==0):
            pass

        elif(self.control.data[0]==1):
            if (deskU.checkFieldOnIncosist(self,1)==True and len(bd.reqExecute(f"Select * from Equipment where Serial_Number='{serialNumber_field.value}'"))==0):
                
                bd.reqExecute(f"""Insert into Equipment(Name,Components,Equipment_Category,Serial_Number,Invetory_Number,Equipment_Status,Cabinet_Number) values(
                              '{(name_field.value)}',
                              '{(components_field.value)}',
                              '{(equipmentCategory_field.value)}',
                              '{(serialNumber_field.value)}',
                              '{(inventoryNumber_field.value)}',
                              '{(equipmentStatus_field.value)}',
                              '{(cabinets_field.value)}',)""")
                
                deskU.successField(self)

            else:
                deskU.errorField(self)

        else:
            if (self.page.overlay[len(self.page.overlay)-1].content.value in [""," "]):
                self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.colors.RED_300
            else:

                if(self.control.data[0]==2):
                    if(len(bd.reqExecute(f"Select * from Cabinets where Number='{self.page.overlay[len(self.page.overlay)-1].content.value}'"))==0):
                        bd.reqExecute(f"Insert into Cabinets(Number) values ('{(self.page.overlay[len(self.page.overlay)-1].content.value)}')")
                        self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.colors.GREEN

                    else:
                        self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.colors.RED_300
                elif(self.control.data[0]==3):
                    if(len(bd.reqExecute(f"Select * from Equipment_Status where Status_Name='{self.page.overlay[len(self.page.overlay)-1].content.value}'"))==0):
                        bd.reqExecute(f"Insert into Equipment_Status(Status_Name) values ('{(self.page.overlay[len(self.page.overlay)-1].content.value)}')")
                        self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.colors.GREEN

                    else:
                        self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.colors.RED_300
                elif(self.control.data[0]==4):
                    if(len(bd.reqExecute(f"Select * from Equipment_Category where Category_Name='{self.page.overlay[len(self.page.overlay)-1].content.value}'"))==0):
                        bd.reqExecute(f"Insert into Equipment_Category(Category_Name) values ('{(self.page.overlay[len(self.page.overlay)-1].content.value)}')")
                        self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.colors.GREEN

                    else:
                        self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.colors.RED_300

        self.page.update()

        time.sleep(0.7)

        self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.colors.BLACK
        self.page.update()

        self_main.control.data[1].updateTable(self)
    
    if(self_main.control.data[0]==0):
        pass #Нужно делать функцию добавления задания от преподователей вручную?

    if(self_main.control.data[0]==1):
        self_main.page.clean()
        
        self_main.page.window.width=1200
        self_main.page.window.height=900

        name_field=ft.TextField(label="Наименование",hint_text="Наименование оборудование",width=300)
        components_field=ft.TextField(label="Компоненты", hint_text="Список компонентов",width=300)
        equipmentCategory_field=ft.DropdownM2(label="Категория",options=[],width=300)

        result=bd.reqExecute("Select * from Equipment_Category")
        for i in result:
            equipmentCategory_field.options.append(ft.dropdownm2.Option(i[0]))

        serialNumber_field=ft.TextField(label="Серийный номер",width=300)
        inventoryNumber_field=ft.TextField(label="Инвентарный номер",width=300)
        equipmentStatus_field=ft.DropdownM2(label="Статус",options=[],width=300)

        result=bd.reqExecute("Select * from Equipment_Status")
        for i in result:
            equipmentStatus_field.options.append(ft.dropdownm2.Option(i[0]))

        cabinets_field=ft.DropdownM2(label="Кабинет", options=[],width=300)

        result=bd.reqExecute("Select * from Cabinets")
        for i in result:
            cabinets_field.options.append(ft.dropdownm2.Option(i[0]))

        addData_button=ft.ElevatedButton("Добавить", on_click=addData,data=self_main.control.data)
        clearFields_button=ft.ElevatedButton("Очистить", on_click=clearFields)
        backButton=ft.IconButton(ft.icons.ARROW_BACK,on_click=lambda _: equipment_page(self_main.page))

        self_main.page.add(ft.Row([backButton]),name_field,components_field,equipmentCategory_field,serialNumber_field,inventoryNumber_field,equipmentStatus_field,cabinets_field,ft.Row([addData_button,clearFields_button],spacing=15,alignment=ft.MainAxisAlignment.CENTER))

    elif(self_main.control.data[0]==2):
        
        cabinetsAdd_dialog=ft.AlertDialog(title=ft.Text("Добавление кабинета"),content=ft.TextField(hint_text="Номер кабинета",width=300), actions=[
            ft.ElevatedButton("Добавить",on_click=addData,data=self_main.control.data,width=100),
            ft.ElevatedButton("Выйти", on_click=lambda _:self_main.page.close(cabinetsAdd_dialog),width=100)
        ])

        self_main.page.open(cabinetsAdd_dialog)

    elif(self_main.control.data[0]==3):
        
        eqCategoryAdd_dialog=ft.AlertDialog(title=ft.Text("Добавление категории оборудования"),content=ft.TextField(hint_text="Наименование категории",width=300), actions=[
            ft.ElevatedButton("Добавить",on_click=addData,data=self_main.control.data,width=100),
            ft.ElevatedButton("Выйти", on_click=lambda _:self_main.page.close(eqCategoryAdd_dialog),width=100)
        ])

        self_main.page.open(eqCategoryAdd_dialog)
        
    elif(self_main.control.data[0]==4):
        
        eqStatusAdd_dialog=ft.AlertDialog(title=ft.Text("Добавление статуса оборудования"),content=ft.TextField(hint_text="Статус оборудования",width=300), actions=[
            ft.ElevatedButton("Добавить",on_click=addData,data=self_main.control.data,width=100),
            ft.ElevatedButton("Выйти", on_click=lambda _:self_main.page.close(eqStatusAdd_dialog),width=100)
        ])

        self_main.page.open(eqStatusAdd_dialog)

    self_main.page.update()

def deleteAllData(self_main):

    def deleteAllData_confirm(self):
        if (type(self_main.page.controls[1].controls[0])!=ft.Text):

            bd.reqExecute(f"Delete from {self.control.data[2]}")

            self_main.page.close(deleteAllData_dialog)
            # self.page.overlay[len(self.page.overlay)-1].content=ft.Text("Удаление прошло успешно", weight=ft.FontWeight.BOLD)
            # self.page.overlay[len(self.page.overlay)-1].actions.pop(0)
            # self.page.overlay[len(self.page.overlay)-1].actions[0].text="Выйти"
            
            if (type(self_main.control.data)!=list):
                    if(int(self_main.control.data.split('|')[3])==0):
                        request_page(self_main.page)
                    elif (int(self_main.control.data.split('|')[3])==1):
                        equipment_page(self_main.page)
                    elif (int(self_main.control.data.split('|')[3])==2):
                        cabinets_page(self_main.page)
                    elif (int(self_main.control.data.split('|')[3])==3):
                        equipmentStatus_page(self_main.page)
                    elif (int(self_main.control.data.split('|')[3])==4):
                        equipmentCategory_page(self_main.page)
            else:
                    if(self_main.control.data[0]==0):
                        request_page(self_main.page)
                    elif(self_main.control.data[0]==1):
                        equipment_page(self_main.page)
                    elif(self_main.control.data[0]==2):
                        cabinets_page(self_main.page)
                    elif(self_main.control.data[0]==3):
                        equipmentStatus_page(self_main.page)
                    elif(self_main.control.data[0]==4):
                        equipmentCategory_page(self_main.page)
        
        deleteAllData_dialog=ft.AlertDialog(title=ft.Text("Подтверждение удаления"), content=ft.Text("Вы действительно хотите удалить все данные из данной таблицы?", weight=ft.FontWeight.BOLD,),
                                            actions=[
                                                ft.ElevatedButton("Да", data=self_main.control.data,on_click=deleteAllData_confirm),
                                                ft.ElevatedButton("Нет", on_click=lambda _:self_main.page.close(deleteAllData_dialog))])
        
        self_main.page.open(deleteAllData_dialog)

def deleteData_page(self_main):

    def deleteData(self):
        
        baseBorderColor=self.page.overlay[len(self.page.overlay)-1].content.border_color

        if (self.page.overlay[len(self.page.overlay)-1].content.value not in [""," ", None]):

            if (self_main.control.data[0]==1):
                bd.reqExecute(f"Delete from Equipment where Serial_Number='{(self.page.overlay[len(self.page.overlay)-1].content.value)}'")
            elif(self_main.control.data[0]==2):
                bd.reqExecute(f"Delete from Cabinets where Number='{(self.page.overlay[len(self.page.overlay)-1].content.value)}'")
            elif(self_main.control.data[0]==3):
                bd.reqExecute(f"Delete from Equipment_Status where Status_Name='{(self.page.overlay[len(self.page.overlay)-1].content.value)}'")
            elif(self_main.control.data[0]==4):
                bd.reqExecute(f"Delete from Equipment_Category where Category_Name='{(self.page.overlay[len(self.page.overlay)-1].content.value)}'")

            self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.colors.GREEN
            self.page.update()

            for i in range(0,len(self.page.overlay[len(self.page.overlay)-1].content.options)-1):
                if (self.page.overlay[len(self.page.overlay)-1].content.options[i].key==self.page.overlay[len(self.page.overlay)-1].content.value):
                    self.page.overlay[len(self.page.overlay)-1].content.options.pop(i)

            time.sleep(0.7)

            self.page.overlay[len(self.page.overlay)-1].content.border_color=baseBorderColor
            self.page.update()
            self_main.control.data[1].updateTable(self_main)

        else:
            self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.colors.RED
            self.page.update()
            time.sleep(0.7)
            self.page.overlay[len(self.page.overlay)-1].content.border_color=baseBorderColor
            self.page.update()




    deleteData_dialog=ft.AlertDialog(title=ft.Text("Удаление данных"),content=ft.DropdownM2(options=[]),actions=[
        ft.ElevatedButton("Удалить", on_click=deleteData,width=100),
        ft.ElevatedButton("Выйти", on_click=lambda _: self_main.page.close(deleteData_dialog),width=100)
    ])

    result=None
    
    if (self_main.control.data[0]==1):
        result=bd.reqExecute("Select Serial_Number from Equipment")

    elif (self_main.control.data[0]==2):
        result=bd.reqExecute("Select Number from Cabinets")

    elif (self_main.control.data[0]==3):
        result=bd.reqExecute("Select Status_Name from Equipment_Status")
            
    elif (self_main.control.data[0]==4):
        result=bd.reqExecute("Select Category_Name from Equipment_Category")

    for dataRes in result:
         deleteData_dialog.content.options.append(ft.dropdownm2.Option(dataRes[0]))

    self_main.page.open(deleteData_dialog)



def equipmentCategory_page(page:ft.Page):
    
    page.clean()

    page.window.width=500
    page.window.height=700

    table_obj=deskU.Table([
        ft.DataColumn(ft.Text("Наименование категории", weight=ft.FontWeight.BOLD, size=13,width=415 ,text_align=ft.TextAlign.CENTER))
        ],500)
    table=table_obj.getTable(4)

    menuBar=ft.MenuBar(
        [
            ft.SubmenuButton(ft.Text("Режимы"), [ft.MenuItemButton(ft.Text("Изменение"),on_click=table_obj.editMode)]),
            ft.SubmenuButton(ft.Text("Функции"), [ft.MenuItemButton(ft.Text("Добавление"),data=[4, table_obj,"Equipment_Category"], on_click=addData_page), 
                                                  ft.SubmenuButton(ft.Text("Удаление"), [ft.MenuItemButton(ft.Text("Запись"),data=[4, table_obj,"Equipment_Category"],on_click=deleteData_page), ft.MenuItemButton(ft.Text("Всё"),data=[4, table_obj,"Equipment_Category"], on_click=deleteAllData)])])],
        style=ft.MenuStyle(ft.alignment.top_left))
    backButton=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: main_page(page))

    if(table!=None):
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar,ft.Divider(1)]),table)
    else:
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar]),ft.Row([ft.Text("На данный момент - таблица является пустой", weight=ft.FontWeight.BOLD,size=20)], alignment=ft.MainAxisAlignment.CENTER,height=500, vertical_alignment=ft.CrossAxisAlignment.CENTER))
    
    page.update()


def equipmentStatus_page(page:ft.Page):
    
    page.clean()

    page.window.width=570
    page.window.height=700

    table_obj=deskU.Table([
        ft.DataColumn(ft.Text("Статус", weight=ft.FontWeight.BOLD, size=16,width=400 ,text_align=ft.TextAlign.CENTER))
        ],500)
    table=table_obj.getTable(3)

    menuBar=ft.MenuBar(
        [
            ft.SubmenuButton(ft.Text("Режимы"), [ft.MenuItemButton(ft.Text("Изменение"),on_click=table_obj.editMode)]),
            # ft.SubmenuButton(ft.Text("Режимы"),[
            #      ft.MenuItemButton(
            #          ft.Chip(ft.Text("Изменение"),on_select=lambda _:page.update())
            #          ),
            #      ],),
            ft.SubmenuButton(ft.Text("Функции"), [ft.MenuItemButton(ft.Text("Добавление"),data=[3,table_obj,"Equipment_Status"], on_click=addData_page), 
                                                  ft.SubmenuButton(ft.Text("Удаление"), [ft.MenuItemButton(ft.Text("Запись"),data=[3,table_obj,"Equipment_Status"],on_click=deleteData_page), ft.MenuItemButton(ft.Text("Всё"),data=[3,table_obj,"Equipment_Status"], on_click=deleteAllData)])])],
        style=ft.MenuStyle(ft.alignment.top_left))
    backButton=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: main_page(page))

    if(table!=None):
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar,ft.Divider(1)]),table)
    else:
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar]),ft.Row([ft.Text("На данный момент - таблица является пустой", weight=ft.FontWeight.BOLD,size=20)], alignment=ft.MainAxisAlignment.CENTER,height=500, vertical_alignment=ft.CrossAxisAlignment.CENTER))
    
    page.update()


def cabinets_page(page:ft.Page):
    
    page.clean()

    page.window.width=400
    page.window.height=700

    table_obj=deskU.Table([
        ft.DataColumn(ft.Text("Номер кабинета", weight=ft.FontWeight.BOLD, size=13,width=260 ,text_align=ft.TextAlign.CENTER))
        ],300)
    table=table_obj.getTable(2)

    menuBar=ft.MenuBar(
        [
            ft.SubmenuButton(ft.Text("Режимы"), [ft.MenuItemButton(ft.Text("Изменение"), on_click=table_obj.editMode)]),
            ft.SubmenuButton(ft.Text("Функции"), [ft.MenuItemButton(ft.Text("Добавление"),data=[2,table_obj,"Cabinets"], on_click=addData_page), 
                                                  ft.SubmenuButton(ft.Text("Удаление"), [ft.MenuItemButton(ft.Text("Запись"),data=[2,table_obj,"Cabinets"],on_click=deleteData_page), ft.MenuItemButton(ft.Text("Всё"), data=[2,table_obj,"Cabinets"],on_click=deleteAllData)])])],
        style=ft.MenuStyle(ft.alignment.top_left))
    backButton=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: main_page(page))

    if(table!=None):
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar,ft.Divider(1)]),table)
    else:
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar]),ft.Row([ft.Text("На данный момент - таблица является пустой", weight=ft.FontWeight.BOLD,size=15)], alignment=ft.MainAxisAlignment.CENTER,height=500, vertical_alignment=ft.CrossAxisAlignment.CENTER))
    
    page.update()


def request_page(page:ft.Page):

    page.clean()

    page.window.width=1400
    page.window.height=700

    table_obj=deskU.Table([
        ft.DataColumn(ft.Text("Номер заявки", weight=ft.FontWeight.BOLD, size=13,width=130 ,text_align=ft.TextAlign.CENTER)),
        ft.DataColumn(ft.Text("ID пользователя", weight=ft.FontWeight.BOLD, size=13,width=130 ,text_align=ft.TextAlign.CENTER)),
        ft.DataColumn(ft.Text("Имя пользователя", weight=ft.FontWeight.BOLD, size=13,width=130 ,text_align=ft.TextAlign.CENTER)), 
        ft.DataColumn(ft.Text("Кабинет", weight=ft.FontWeight.BOLD, size=13,width=130 ,text_align=ft.TextAlign.CENTER)), 
        ft.DataColumn(ft.Text("Описание заявки", weight=ft.FontWeight.BOLD, size=13,width=130 ,text_align=ft.TextAlign.CENTER)), 
        ft.DataColumn(ft.Text("Статус заявки", weight=ft.FontWeight.BOLD, size=13,width=130 ,text_align=ft.TextAlign.CENTER))
        ],1200)
    table=table_obj.getTable(0)

    menuBar=ft.MenuBar(
        [
            ft.SubmenuButton(ft.Text("Режимы"), [ft.MenuItemButton(ft.Text("Изменение"),on_click=table_obj.editMode)]),
            ft.SubmenuButton(ft.Text("Функции"), [ft.MenuItemButton(ft.Text("Добавление"),data=[0,table_obj,"Repair_Request"], on_click=addData_page), 
                                                  ft.SubmenuButton(ft.Text("Удаление"), [ft.MenuItemButton(ft.Text("Запись"),data=[0,table_obj,"Repair_Request"],on_click=deleteData_page), ft.MenuItemButton(ft.Text("Всё"), data=[0,table_obj,"Repair_Request"],on_click=deleteAllData)])])],
        style=ft.MenuStyle(ft.alignment.top_left))
    backButton=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: main_page(page))

    if(table!=None):
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar]),table)
    else:
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar]),ft.Row([ft.Text("На данный момент - таблица является пустой", weight=ft.FontWeight.BOLD,size=20)], alignment=ft.MainAxisAlignment.CENTER,height=500, vertical_alignment=ft.CrossAxisAlignment.CENTER))
    
    page.update()


def equipment_page(page:ft.Page):

    page.clean()

    page.window.width=1400
    page.window.height=700

    table_obj=deskU.Table([
        ft.DataColumn(ft.Text("Название", weight=ft.FontWeight.BOLD, size=13,width=130 ,text_align=ft.TextAlign.CENTER)), 
        ft.DataColumn(ft.Text("Компоненты", weight=ft.FontWeight.BOLD, size=13,width=130 ,text_align=ft.TextAlign.CENTER)), 
        ft.DataColumn(ft.Text("Категория", weight=ft.FontWeight.BOLD, size=13,width=130 ,text_align=ft.TextAlign.CENTER)), 
        ft.DataColumn(ft.Text("Серийный номер", weight=ft.FontWeight.BOLD, size=13,width=130 ,text_align=ft.TextAlign.CENTER)), 
        ft.DataColumn(ft.Text("Инвентарный номер", weight=ft.FontWeight.BOLD, size=13,width=130 ,text_align=ft.TextAlign.CENTER)), 
        ft.DataColumn(ft.Text("Статус", weight=ft.FontWeight.BOLD, size=13,width=130 ,text_align=ft.TextAlign.CENTER)), 
        ft.DataColumn(ft.Text("Местонахождение", weight=ft.FontWeight.BOLD, size=13,width=130 ,text_align=ft.TextAlign.CENTER))],1300)
    
    table=table_obj.getTable(1)

    menuBar=ft.MenuBar(
        [
            ft.SubmenuButton(ft.Text("Режимы"), [ft.MenuItemButton(ft.Text("Изменение"),on_click=table_obj.editMode)]),
            ft.SubmenuButton(ft.Text("Функции"), [
                ft.MenuItemButton(ft.Text("Добавление"), data=[1,table_obj,"Equipment"],on_click=addData_page), 
                ft.SubmenuButton(ft.Text("Удаление"), [ft.MenuItemButton(ft.Text("Запись"), data=[1,table_obj,"Equipment"] ,on_click=deleteData_page), ft.MenuItemButton(ft.Text("Всё"), data=[1,table_obj,"Equipment"] ,on_click=deleteAllData)])])],
        style=ft.MenuStyle(ft.alignment.top_left))
    backButton=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: main_page(page))

    if(table!=None):
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar]),table)
    else:
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar]),ft.Row([ft.Text("На данный момент - таблица является пустой",weight=ft.FontWeight.BOLD,size=20)], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER))
    
    page.update()

    pass


def main_page(page:ft.Page):
    
    page.clean()

    page.window.width=1280
    page.window.height=960

    requestPageButton=ft.ElevatedButton("Заявки", icon=ft.icons.HOME_REPAIR_SERVICE, width=130, on_click=lambda _:request_page(page))
    equipmentPageButton=ft.ElevatedButton("Оборудование", icon=ft.icons.LAPTOP_CHROMEBOOK, width=150, on_click= lambda _:equipment_page(page))
    cabinetsButton=ft.ElevatedButton("Кабинеты", on_click=lambda _:cabinets_page(page),width=130, icon=ft.icons.ROOM)
    equipmentStatusButton=ft.ElevatedButton("Статус оборудования", on_click=lambda _: equipmentStatus_page(page),width=200, icon=ft.icons.ARCHIVE)
    equipmentCategoryButton=ft.ElevatedButton("Категории оборудования", on_click=lambda _:equipmentCategory_page(page),width=200, icon=ft.icons.SEGMENT)
    

    page.add(
        ft.Row([requestPageButton,equipmentPageButton], spacing=20, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Row([cabinetsButton,equipmentStatusButton],spacing=20, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Row([equipmentCategoryButton], alignment=ft.MainAxisAlignment.CENTER))
    logger_pages.info("'Main' page was openned")
    page.update()


def resetPassword_page(page: ft.Page):

    def resetPassword_handler(self):

        try:
            if (userIdField.value!="\n" or userIdField.value!=""):
                usernameReq=bd.reqExecute(f"Select Username from Users where TG_ID={userIdField.value}")
                baseColor=userIdField.border_color

                if (type(page.controls[4])==ft.Column):
                    page.controls.pop(4)

                if(len(usernameReq)!=0):
                    result=bd.reqExecute(f"Select * from Administrators where TG_Username='{usernameReq[0][0]}'")
                    if (result!=False and len(result)!=0):
                        req=requests.post("https://api.telegram.org/bot7527441182:AAEI1sSafhOnZ1oLgeRgdaJALzxoHEmiWLY/sendMessage", data={"chat_id":userIdField.value, "text": f'Ваш пароль: {result[0][2]}'})
                        if (req.status_code==200):
                            userIdField.border_color=ft.colors.GREEN
                        else:
                            userIdField.border_color=ft.colors.RED
                            errorLabel.value="Произошла ошибка при отправке запроса"
                            page.controls.insert(4,ft.Column([ft.Text("",height=20), errorLabel]))
                    else:
                        userIdField.border_color=ft.colors.RED
                        errorLabel.value="Не имеется администратора с данным ID"
                        page.controls.insert(4,ft.Column([ft.Text("",height=20), errorLabel]))
                else:
                    userIdField.border_color=ft.colors.RED
                    errorLabel.value="Данное ID не зарегистрировано в базе данных приложения"
                    page.controls.insert(4,ft.Column([ft.Text("",height=20), errorLabel]))

            else:
                userIdField.border_color=ft.colors.RED

            self.page.update()
            time.sleep(0.7)

            userIdField.border_color=baseColor
            self.page.update()

        except Exception as ex:

            logger_pages.exception(f" {ex}")
            page.window.bgcolor=ft.colors.RED
            page.update()

            time.sleep(0.7)

            page.window.bgcolor=ft.colors.TRANSPARENT
            page.update()

    page.clean()

    information_Text_1=ft.Text("Забыли пароль?", size=30, selectable=False,weight=ft.FontWeight.BOLD,font_family="Main Label", text_align=ft.TextAlign.CENTER)
    information_Text_2=ft.Text("Для восстановления пароля нужно ввести ID, который привязан к профилю Telegram", size=14, selectable=False,font_family="Moderustic Light",width=230,text_align=ft.TextAlign.CENTER)

    userIdField=ft.TextField(
        hint_text="Telegram ID", 
        hint_style=ft.TextStyle(font_family="Moderustic Light"),
        max_lines=1,
        text_style=ft.TextStyle(font_family="Moderustic Regular"),
        border_radius=14, 
        border_color=deskU.ui_colors[0],
        on_focus=deskU.contentColor_focus,
        on_blur=deskU.contentColor_blur,
        width=200
        )
    resetPasswButton=ft.ElevatedButton(
        "Сбросить пароль", 
        icon=ft.icons.RESTART_ALT_OUTLINED,
        icon_color=ft.colors.WHITE,
        bgcolor=deskU.ui_colors[1],
        color=ft.colors.WHITE,
        on_click=resetPassword_handler)
    
    findIDButton=ft.ElevatedButton(
        "Узнать свой ID",
        bgcolor=deskU.ui_colors[0],
        color=ft.colors.BLACK,
        on_click=lambda _:page.launch_url("https://t.me/userinfobot?start=info")
    )

    errorLabel=ft.Text("", font_family="Moderustic Regular", size=13,disabled=True,height=30)

    backPageButton=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: start_page(page), visible=True, icon_color=deskU.ui_colors[1], splash_radius=10)

    page.add(
        ft.Row([backPageButton],alignment=ft.MainAxisAlignment.START),
        ft.Column([information_Text_1, information_Text_2], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Text("", height=20),
        userIdField,resetPasswButton,findIDButton)
    logger_pages.info("'Reset password' page was openned")
    page.update()


def start_page(page:ft.Page, fromRegistr:bool=False):

    def nextPage(self):
        result=bd.reqExecute(f"Select * from Administrators where Login='{(sha384(loginField.value.encode()).hexdigest())}' OR TG_Username='{(sha384(loginField.value.encode()).hexdigest())}' AND Password='{(sha384(passwordField.value.encode()).hexdigest())}'")
        if (len(result)!=0):
            main_page(self.page)
        else:
            deskU.errorField(self)

    def resetPassword(self):
        resetPassword_page(self.page)

    page.clean()

    if (fromRegistr==False):

        page.window.width=800
        page.window.height=700

        page.title="НАМТ.Администраторы"
        page.theme_mode=ft.ThemeMode.LIGHT
        page.vertical_alignment=ft.MainAxisAlignment.CENTER
        page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
        page.window.resizable=False
        page.window.prevent_close=True
        page.window.on_event=deskU.pageClose

        page.fonts={
        'Main Label': 'Fonts\\TechMonoRegular.otf',
        'Moderustic Bold': 'Fonts\\Moderustic\\Moderustic-Bold.ttf',
        'Moderustic Light':'Fonts\\Moderustic\\Moderustic-Light.ttf',
        'Moderustic Regular':'Fonts\\Moderustic\\Moderustic-Regular.ttf'}

        page.decoration=ft.BoxDecoration(image=ft.DecorationImage("Desktop\\Image\\Background.jpg", fit=ft.ImageFit.CONTAIN),shape=ft.BoxShape.RECTANGLE)

    startLabel=ft.Text("Вход", size=30,font_family="Main Label",text_align=ft.TextAlign.CENTER)
    startDescriptionLabel=ft.Text("", width=280, size=13, font_family="Moderustic Regular", text_align=ft.TextAlign.CENTER)
    
    loginField=ft.TextField(
        hint_text="Логин или Telegram", 
        width=200,
        max_lines=1,
        text_style=ft.TextStyle(font_family="Moderustic Regular"),
        border_radius=14, 
        border_color=deskU.ui_colors[0],
        on_focus=deskU.contentColor_focus,
        on_blur=deskU.contentColor_blur)
    passwordField=ft.TextField(
        hint_text="Пароль",
        width=200, 
        password=True,
        max_lines=1,
        text_style=ft.TextStyle(font_family="Moderustic Regular"),
        border_radius=14, 
        border_color=deskU.ui_colors[0],
        on_focus=deskU.contentColor_focus,
        on_blur=deskU.contentColor_blur)
    enterButton=ft.ElevatedButton(
        "Войти",
        on_click=nextPage, 
        width=100,
        bgcolor=deskU.ui_colors[1],
        color=ft.colors.WHITE)
    
    resetPasswordButton=ft.ElevatedButton("Забыли пароль?", width=150, on_click=resetPassword, bgcolor=ft.colors.WHITE)
    registrPasswordButton=ft.ElevatedButton("Регистрация", width=150, on_click=lambda _:startAdmin_page(page), bgcolor="#8FA2CA",color=ft.colors.WHITE)

    page.add(ft.Column([startLabel,startDescriptionLabel],spacing=5,horizontal_alignment=ft.CrossAxisAlignment.CENTER),ft.Text("",height=30),loginField,passwordField,enterButton,ft.Text("",height=20),ft.Row([registrPasswordButton,resetPasswordButton],spacing=15,alignment=ft.MainAxisAlignment.CENTER))

    if(os.path.isfile("Desktop\\Admin Configure")==True):

        with open("Desktop\\Admin Configure", 'r') as File:
            line=File.readlines()
            if (line[0]=="Enter Today:1"):
                startDescriptionLabel.value=deskU.login_coLabelText[randint(0,len(deskU.login_coLabelText)-1)]
            elif (line[0]!=f"Enter Today:{datetime.datetime.now().strftime('%D')}"):
                startDescriptionLabel.value=deskU.login_coLabelText[2]
            else:
                startDescriptionLabel.value=deskU.login_coLabelText[1]

    else:

        startDescriptionLabel.value="Вы здесь в первый раз?\nДля дальнейшей работы вам необходимо зарегистрироваться или войти в аккаунт"
        registrPasswordButton.focus()

    logger_pages.info("'Start' page was openned")
    page.window.center()
    page.update()


def startAdmin_page(page:ft.Page):

    def backPage(self):

        start_page(self.page,True)

    def adminRegInBD(self):

        result=bd.reqExecute(f"Select * from Administrators where TG_Username='{sha384(usernameField.value.encode()).hexdigest()}' AND FSL='{(fslField.value)}' AND Mac_Address='{hex(uuid.getnode())}'")

        if((fslField.value!="" and len(fslField.value.split(" "))==3) and (loginField.value!="" and len(loginField.value)<=255) and deskU.dynamicPassCheck(self,False)==True and (usernameField.value!="" and usernameField.value.find("@")==-1)):

            if (len(result)==0):

                result=bd.reqExecute(f"Insert into Administrators(FSL,Login, Mac_Address,Password, TG_Username) values ('{(fslField.value)}', '{sha384(loginField.value.encode()).hexdigest()}', '{hex(uuid.getnode())}' ,'{sha384(passwordField.value.encode()).hexdigest()}', '{sha384(usernameField.value.encode()).hexdigest()}')")

                if (result!=False):

                    with open("Desktop\\Admin Configure", 'w') as bFile:
                        bFile.write(f"Enter Today: 1")

                    for i in range(1,len(self.page.controls)):
                        self.page.controls[i].disabled=True
                    
                    deskU.successField(self)

                else:

                    deskU.errorField(self)

            else:
                usernameField.border_color=ft.colors.RED_300
                fslField.border_color=ft.colors.RED_300
                failedRegistLabel.value="Возможно неверно заполенные данные\nили данное устройство уже зарегистрировано в приложении"

                self.page.update()
                time.sleep(0.7)

                usernameField.border_color=ft.colors.BLACK
                fslField.border_color=ft.colors.BLACK
                failedRegistLabel.value=""
                self.page.update()

        else:
            baseColor=self.page.controls[3].border_color
            deskU.checkFieldOnIncosist(self,0)

            if (page.controls[6].border_color!=ft.colors.RED):
                page.controls[6].border_color=ft.colors.RED
                page.update()

            time.sleep(0.7)

        for control in self.page.controls:
                if (type(control)==ft.TextField):
                    control.border_color=baseColor
        self.page.update()
            

    page.clean()

    page.window.width=800
    page.window.height=700

    # page.fonts={
    #     'Main Label': 'Fonts\\TechMonoRegular.otf',
    #     'Moderustic Bold': 'Fonts\\Moderustic\\Moderustic-Bold.ttf',
    #     'Moderustic Light':'Fonts\\Moderustic\\Moderustic-Light.ttf',
    #     'Moderustic Regular':'Fonts\\Moderustic\\Moderustic-Regular.ttf'}

    startLabel=ft.Text("Создание аккаунта", size=30,font_family="Main Label")
    startDescriptionLabel=ft.Text("Заполните необходимые поля,\nчтобы получить полноценный доступ \nк приложению", width=280, size=13, font_family="Moderustic Regular", text_align=ft.TextAlign.CENTER)

    fslField=ft.TextField(
        hint_text="ФИО администратора",
        width=210,
        hint_style=ft.TextStyle(font_family="Moderustic Regular"),
        border_radius=14,
        max_lines=1, 
        border_color=deskU.ui_colors[0],
        on_focus=deskU.contentColor_focus,
        on_blur=deskU.contentColor_blur)
    
    loginField=ft.TextField(
        hint_text="Логин", 
        width=210,
        hint_style=ft.TextStyle(font_family="Moderustic Regular"),
        border_radius=14, 
        max_lines=1, 
        border_color=deskU.ui_colors[0],
        on_focus=deskU.contentColor_focus,
        on_blur=deskU.contentColor_blur)
    
    usernameField=ft.TextField(
        hint_text="Имя пользователя", 
        width=210, label="Telegram",
        hint_style=ft.TextStyle(font_family="Moderustic Regular"),
        border_radius=14, 
        max_lines=1, 
        border_color=deskU.ui_colors[0],
        on_focus=deskU.contentColor_focus,
        on_blur=deskU.contentColor_blur)
    
    passwordField=ft.TextField(
        hint_text="Пароль", 
        width=210, 
        password=True, 
        on_change=deskU.dynamicPassCheck,
        hint_style=ft.TextStyle(font_family="Moderustic Regular"),
        border_radius=14, 
        max_lines=1, 
        border_color=deskU.ui_colors[0],
        on_focus=deskU.contentColor_focus,
        on_blur=deskU.contentColor_blur)
    
    failedRegistLabel=ft.Text("", font_family="Moderustic Regular",size=13)

    regirtrAdminButton=ft.ElevatedButton("Зарегистрироваться", width=165, on_click=adminRegInBD, bgcolor=deskU.ui_colors[1],color=ft.colors.WHITE)
    backPageButton=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=backPage, icon_color=deskU.ui_colors[1], splash_radius=10)

    #Для записи токена инициализации шифрования в байтовой форме
    # with open("adminConfig", "wb"):

    #     pass

    #page.add(ft.Row([backPageButton]),ft.Column([fslField,loginField,usernameField,passwordField,regirtrAdminButton], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=800,height=700))
    page.add(
        ft.Row([backPageButton], alignment=ft.MainAxisAlignment.START),
        ft.Column([startLabel,startDescriptionLabel],spacing=5),
        ft.Text("",height=30) ,
        fslField,loginField,usernameField,passwordField,regirtrAdminButton,
        ft.Text("", height=30),
        failedRegistLabel)
    logger_pages.info("'StartAdmin' page was openned")
    page.update()