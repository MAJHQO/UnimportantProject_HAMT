import flet as ft, time, logging,datetime,os
from utilits import bd,utilits_desktop as deskU
from random import randint
from utilits.bd import db_object

import uuid,pandas as pd

from hashlib import sha384



logger_pages=logging.getLogger("pages")
logger_pages.setLevel(logging.INFO)

def addData_page(self_main):

    def clearFields(self):
        
        for i in range(1, len(self.page.controls)):
            self.page.controls[i].value=""

        self.page.update()

    def addData(self):
        if(self.control.data[0]==1):
            if (len(db_object.request_execute(f"Select * from Equipment where Serial_Number Like'{serialNumber_field.value}'"))==0):
                if(deskU.checkEqAdd_OnIncosist(self_main.page.controls[1].controls)):
                    db_object.request_execute(f"""Insert into Equipment(Name,IP_Address,MAC_Address,CPU_Model,CPU_Frequency,Network_Name,RAM,HDD,Equipment_Category,Serial_Number,Invetory_Number,Equipment_Status,Cabinet_Number) values(
                                '{(name_field.value)}',
                                '{(ip_field.value)}',
                                '{(mac_field.value)}',
                                '{(cpuModel_field.value)}',
                                '{(cpuFreq_field.value)}',
                                '{(networkName_field.value)}',
                                {(ram_field.value)},
                                {(hdd_field.value)},
                                '{(equipmentCategory_field.value)}',
                                '{(serialNumber_field.value)}',
                                '{(inventoryNumber_field.value)}',
                                '{(equipmentStatus_field.value)}',
                                '{(cabinets_field.value)}')""")
                    deskU.successField(self)
                    equipmentCategory_field.border_color=self.page.controls[1].border_color
                    equipmentStatus_field.border_color=self.page.controls[1].border_color
                    cabinets_field.border_color=self.page.controls[1].border_color
                else:
                    deskU.errorDialog(self_main.page,"Введенные данные являются логически неправильными или неподходящими по формату")
            else:
                deskU.errorField(self)


        else:
            if (self.page.overlay[len(self.page.overlay)-1].content.value in [""," "]):
                self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.Colors.RED_300
            else:

                if(self.control.data[0]==2):
                    if(len(db_object.request_execute(f"Select * from Cabinets where Number='{self.page.overlay[len(self.page.overlay)-1].content.value}'"))==0):
                        db_object.request_execute(f"Insert into Cabinets(Number) values ('{(self.page.overlay[len(self.page.overlay)-1].content.value)}')")
                        self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.Colors.GREEN

                    else:
                        self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.Colors.RED_300
                elif(self.control.data[0]==3):
                    if(len(db_object.request_execute(f"Select * from Equipment_Status where Status_Name='{self.page.overlay[len(self.page.overlay)-1].content.value}'"))==0):
                        db_object.request_execute(f"Insert into Equipment_Status(Status_Name) values ('{(self.page.overlay[len(self.page.overlay)-1].content.value)}')")
                        self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.Colors.GREEN

                    else:
                        self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.Colors.RED_300
                elif(self.control.data[0]==4):
                   
                    if(len(db_object.request_execute(f"Select * from Equipment_Category where Category_Name='{self.page.overlay[len(self.page.overlay)-1].content.value}'"))==0):
                        db_object.request_execute(f"Insert into Equipment_Category(Category_Name) values ('{(self.page.overlay[len(self.page.overlay)-1].content.value)}')")

                        self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.Colors.GREEN

                    else:
                        self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.Colors.RED_300
            self.page.update()

            time.sleep(0.7)

            self.page.overlay[len(self.page.overlay)-1].content.border_color=ft.Colors.BLACK
            deskU.page_update(self.page,self.control.data[1])
            self.page.update()

    if(self_main.control.data[0]==1):
        self_main.page.clean()
        
        self_main.page.window.width=1200
        self_main.page.window.height=900

        name_field=ft.TextField(label="Наименование",hint_text="Наименование оборудование",width=300)
        ip_field=ft.TextField(label="IP-адрес", hint_text="IP-адрес оборудования",width=300)
        mac_field=ft.TextField(label="Mac-адрес", hint_text="Mac-адрес оборудования",width=300)
        cpuModel_field=ft.TextField(label="Процессор", hint_text="Модель процессора",width=300)
        cpuFreq_field=ft.TextField(label="Частота", hint_text="Частота процессора",width=300)
        networkName_field=ft.TextField(label="Имя в сети", width=300)
        ram_field=ft.TextField(label="RAM", hint_text="Объем ОЗУ",width=300)
        hdd_field=ft.TextField(label="HDD", hint_text="Объем ЖД",width=300)
        equipmentCategory_field=ft.DropdownM2(label="Категория",options=[],width=300)

        result=db_object.request_execute("Select * from Equipment_Category")
        for i in result:
            equipmentCategory_field.options.append(ft.dropdownm2.Option(i[1]))

        serialNumber_field=ft.TextField(label="Серийный номер",width=300)
        inventoryNumber_field=ft.TextField(label="Инвентарный номер",width=300)
        equipmentStatus_field=ft.DropdownM2(label="Статус",options=[],width=300)

        result=db_object.request_execute("Select * from Equipment_Status")
        for i in result:
            equipmentStatus_field.options.append(ft.dropdownm2.Option(i[1]))

        cabinets_field=ft.DropdownM2(label="Кабинет", options=[],width=300)

        result=db_object.request_execute("Select * from Cabinets")
        for i in result:
            cabinets_field.options.append(ft.dropdownm2.Option(i[1]))

        addData_button=ft.ElevatedButton("Добавить", on_click=addData,data=self_main.control.data)
        clearFields_button=ft.ElevatedButton("Очистить", on_click=clearFields)
        backButton=ft.IconButton(ft.Icons.ARROW_BACK,on_click=lambda _: equipment_page(self_main.page))

        self_main.page.add(
            ft.Row([backButton]),
            ft.Column([
                name_field,
                ip_field,
                mac_field,
                cpuModel_field,
                cpuFreq_field,
                networkName_field,
                ram_field,
                hdd_field,
                equipmentCategory_field,
                serialNumber_field,
                inventoryNumber_field
                ,equipmentStatus_field,
                cabinets_field,
                ft.Row([addData_button,clearFields_button],spacing=15,alignment=ft.MainAxisAlignment.CENTER)    
            ], scroll=True, height=700, horizontal_alignment=ft.CrossAxisAlignment.CENTER))

    elif(self_main.control.data[0]==2):
        
        cabinetsAdd_dialog=ft.AlertDialog(title=ft.Text("Добавление кабинета"),content=ft.TextField(hint_text="Номер кабинета",width=300), actions=[
            ft.ElevatedButton("Добавить",on_click=addData,data=self_main.control.data,width=100),
            ft.ElevatedButton("Выйти", on_click=lambda _:self_main.page.close(cabinetsAdd_dialog),width=100)
        ])

        self_main.page.open(cabinetsAdd_dialog)

    elif(self_main.control.data[0]==4):
        
        eqCategoryAdd_dialog=ft.AlertDialog(title=ft.Text("Добавление категории оборудования"),content=ft.TextField(hint_text="Наименование категории",width=300), actions=[
            ft.ElevatedButton("Добавить",on_click=addData,data=self_main.control.data,width=100),
            ft.ElevatedButton("Выйти", on_click=lambda _:self_main.page.close(eqCategoryAdd_dialog),width=100)
        ])

        self_main.page.open(eqCategoryAdd_dialog)
        
    elif(self_main.control.data[0]==3):
        
        eqStatusAdd_dialog=ft.AlertDialog(title=ft.Text("Добавление статуса оборудования"),content=ft.TextField(hint_text="Статус оборудования",width=300), actions=[
            ft.ElevatedButton("Добавить",on_click=addData,data=self_main.control.data,width=100),
            ft.ElevatedButton("Выйти", on_click=lambda _:self_main.page.close(eqStatusAdd_dialog),width=100)
        ])

        self_main.page.open(eqStatusAdd_dialog)

    self_main.page.update()

def deleteAllData(self_main):

    def deleteAllData_confirm(self):
        if (type(self_main.page.controls[1].controls[0])!=ft.Text):

            db_object.request_execute(f"Delete from {self.control.data[2]}")

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
                    elif (int(self_main.control.data.split('|')[3])==5):
                        manageAdminAcc_page(self_main.page)
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
                    elif(self_main.control.data[0]==5):
                        manageAdminAcc_page(self_main.page)
        
    deleteAllData_dialog=ft.AlertDialog(title=ft.Text("Подтверждение удаления"), content=ft.Text("Вы действительно хотите удалить все данные из данной таблицы?", weight=ft.FontWeight.BOLD,),
                                            actions=[
                                                ft.ElevatedButton("Да", data=self_main.control.data,on_click=deleteAllData_confirm),
                                                ft.ElevatedButton("Нет", on_click=lambda _:self_main.page.close(deleteAllData_dialog))])
        
    self_main.page.open(deleteAllData_dialog)

def equipmentCategory_page(page:ft.Page):
    
    page.clean()

    page.window.width=820
    page.window.height=700

    table_obj=db_object.get_table_obj('equipment_category')
    table=table_obj.getTable(db_object)

    menuBar=ft.MenuBar(
        [
            ft.SubmenuButton(ft.Text("Функции"), [ft.MenuItemButton(ft.Text("Добавление"),data=[4, table_obj,"Equipment_Category"], on_click=addData_page), 
                                                  ft.SubmenuButton(ft.Text("Удаление"), [ft.MenuItemButton(ft.Text("Всё"),data=[4, table_obj,"Equipment_Category"], on_click=deleteAllData)])])],
        style=ft.MenuStyle(ft.alignment.top_left))
    backButton=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: main_page_v2(page))

    if(table!=False):
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar,ft.Divider(1)]),table)
    else:
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar]),ft.Row([ft.Text("На данный момент - таблица является пустой", weight=ft.FontWeight.BOLD,size=20)], alignment=ft.MainAxisAlignment.CENTER,height=500, vertical_alignment=ft.CrossAxisAlignment.CENTER))
    
    page.window.center()
    page.update()


def equipmentStatus_page(page:ft.Page):
    
    page.clean()

    page.window.width=900
    page.window.height=700

    table_obj=db_object.get_table_obj('equipment_status')
    table=table_obj.getTable(db_object)

    menuBar=ft.MenuBar(
        [
            ft.SubmenuButton(ft.Text("Функции"), [ft.MenuItemButton(ft.Text("Добавление"),data=[3,table_obj,"Equipment_Status"], on_click=addData_page), 
                                                  ft.SubmenuButton(ft.Text("Удаление"), [ft.MenuItemButton(ft.Text("Всё"),data=[3,table_obj,"Equipment_Status"], on_click=deleteAllData)])])],
        style=ft.MenuStyle(ft.alignment.top_left))
    backButton=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: main_page_v2(page))

    if(table!=False):
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar,ft.Divider(1)]),table)
    else:
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar]),ft.Row([ft.Text("На данный момент - таблица является пустой", weight=ft.FontWeight.BOLD,size=20)], alignment=ft.MainAxisAlignment.CENTER,height=500, vertical_alignment=ft.CrossAxisAlignment.CENTER))
    
    page.window.center()
    page.update()


def cabinets_page(page:ft.Page):
    
    page.clean()

    page.window.width=830
    page.window.height=700

    table_obj=db_object.get_table_obj('cabinets')
    table=table_obj.getTable(db_object)


    menuBar=ft.MenuBar(
        [
            ft.SubmenuButton(ft.Text("Функции"), [ft.MenuItemButton(ft.Text("Добавление"),data=[2,table_obj,"Cabinets"], on_click=addData_page), 
                                                  ft.SubmenuButton(ft.Text("Удаление"), [ft.MenuItemButton(ft.Text("Всё"), data=[2,table_obj,"Cabinets"],on_click=deleteAllData)])])],
        style=ft.MenuStyle(ft.alignment.top_left))
    backButton=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: main_page_v2(page))

    if(table!=False):
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar,ft.Divider(1)]),table)
    else:
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar]),ft.Row([ft.Text("На данный момент - таблица является пустой", weight=ft.FontWeight.BOLD,size=15)], alignment=ft.MainAxisAlignment.CENTER,height=500, vertical_alignment=ft.CrossAxisAlignment.CENTER))
    
    page.window.center()
    page.update()


def request_page(page:ft.Page):

    page.clean()

    page.window.width=1400
    page.window.height=700

    table_obj=db_object.get_table_obj('repair_request')
    table=table_obj.getTable(db_object)

    menuBar=ft.MenuBar(
        [
            ft.SubmenuButton(ft.Text("Режимы"), [ft.MenuItemButton(ft.Text("Изменение"),on_click=deskU.change_eqPage_Mode)]),
            ft.SubmenuButton(ft.Text("Функции"), [ft.SubmenuButton(ft.Text("Удаление"), [ ft.MenuItemButton(ft.Text("Всё"), data=[0,table_obj,"Repair_Request"],on_click=deleteAllData)])])],
        style=ft.MenuStyle(ft.alignment.top_left))
    backButton=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: main_page_v2(page))

    if(table!=False):
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar]),table)
        deskU.change_eqPage_Mode(page)
    else:
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar]),ft.Row([ft.Text("На данный момент - таблица является пустой", weight=ft.FontWeight.BOLD,size=20)], alignment=ft.MainAxisAlignment.CENTER,height=500, vertical_alignment=ft.CrossAxisAlignment.CENTER))
    
    page.update()


def equipment_page(page:ft.Page):

    def baseMode(self):
        page.controls.pop(len(page.controls)-1)
        self.control.content=ft.Text("Поиск")
        self.control.on_click=searchMode

        page.update()

    def searchMode(self):
        self.control.content=ft.Text("Стандартный")
        self.control.on_click=baseMode

        page.controls.append(ft.TextField(
            hint_text="Поиск...",
            width=350,
            hint_style=ft.TextStyle(font_family="Moderustic Regular",),
            border_radius=14, 
            border_color=deskU.ui_colors[0],
            on_focus=deskU.contentColor_focus,
            on_blur=deskU.contentColor_blur,
            on_change=deskU.searchInTable,
            data=self.control.data
        ))
        page.update()

    def loadExcel_handler(self):
        if (self.files[0].path!="" and self.files[0].path!=None):
            if (self.files[0].path.find("Kompyuterny_park.xls")!=-1 or self.files[0].path.find("Компьютерный_парк.xls")!=-1):
                excel_obj=pd.read_excel(self.files[0].path)
                deskU.loadExcel(page,excel_obj,table_obj)
            else:
                deskU.errorIcon(self.page)
        else:
            deskU.errorIcon(self.page)

    page.clean()

    page.window.width=1200
    page.window.height=700

    table_obj=db_object.get_table_obj('equipment')
    table=table_obj.getTable(db_object)

    menuBar=ft.MenuBar(
        [
            ft.SubmenuButton(ft.Text("Режимы"), [
                ft.MenuItemButton(ft.Text("Изменение"),on_click=table_obj.changeMode_handler),
                ft.MenuItemButton(ft.TextButton("Поиск",icon=ft.Icons.SEARCH, icon_color=ft.Colors.WHITE), on_click=searchMode, data=[1,table_obj])]),
            ft.SubmenuButton(ft.Text("Функции"), [
                ft.MenuItemButton(ft.Text("Добавление"), data=[1,table_obj,"Equipment"],on_click=addData_page), 
                ft.SubmenuButton(ft.Text("Удаление"), [ft.MenuItemButton(ft.Text("Всё"), data=[1,table_obj,"Equipment"] ,on_click=deleteAllData)])])],
        style=ft.MenuStyle(ft.alignment.top_left))
    
    backButton=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: main_page_v2(page))
    loadData=ft.IconButton(
        icon=ft.Icons.UPLOAD_FILE, 
        icon_size=23,tooltip="Подгрузка данных",
        on_click=lambda _:excelPicker_obj.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["xlsx", "xltx", "xltm","xls"])
        )
    
    excelPicker_obj=ft.FilePicker(loadExcel_handler,data=[loadData,page])

    
    if(table!=False):
        page.add(ft.Row([backButton, loadData,ft.Text(" ", width=30),menuBar,ft.Divider(1)]),table,excelPicker_obj)
    else:
        page.add(ft.Row([backButton,loadData,ft.Text(" ", width=30),menuBar]),ft.Row([ft.Text("На данный момент - таблица является пустой", weight=ft.FontWeight.BOLD,size=17)], alignment=ft.MainAxisAlignment.CENTER,height=500, vertical_alignment=ft.CrossAxisAlignment.CENTER),excelPicker_obj)
    
    page.window.center()
    page.update()


def manageAdminAcc_page(page: ft.Page):
    page.clean()

    page.window.width=1250
    page.window.height=700

    table_obj=db_object.get_table_obj('administrators')
    table=table_obj.getTable(db_object)

    menuBar=ft.MenuBar(
        [
            ft.SubmenuButton(ft.Text("Функции"), [
                ft.SubmenuButton(ft.Text("Удаление"), [ 
                    ft.MenuItemButton(ft.Text("Всё"), data=[5,table_obj,"Equipment"] ,on_click=deleteAllData)]
                    )]
                    )],
        style=ft.MenuStyle(ft.alignment.top_left))
    backButton=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: main_page_v2(page))

    if(table!=False):
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar]),table)
    else:
        page.add(ft.Row([backButton,ft.Text(" ", width=30),menuBar]),ft.Row([ft.Text("На данный момент - таблица является пустой",weight=ft.FontWeight.BOLD,size=20)], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER))
    
    page.window.center()
    page.update() 


def main_page_v2(page:ft.Page):
    try:
        page.clean()

        page.window.width=1280
        page.window.height=800
        page.window.resizable=True
        page.update()


        requestPageButton=ft.ElevatedButton(
            "Заявки", 
            icon=ft.Icons.HOME_REPAIR_SERVICE,
            width=220,
            on_click=lambda _:request_page(page),
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT:"#F0F0F8", ft.ControlState.HOVERED:"#778FD2"},
                animation_duration=200,
                shape={ft.ControlState.DEFAULT:ft.RoundedRectangleBorder(3), ft.ControlState.HOVERED: ft.RoundedRectangleBorder(20)},
                icon_color={ft.ControlState.DEFAULT: "0d1611", ft.ControlState.HOVERED: "#ffffff"},
                color={ft.ControlState.DEFAULT: "0d1611", ft.ControlState.HOVERED: "#ffffff"}))
        equipmentPageButton=ft.ElevatedButton(
            "Оборудование", 
            icon=ft.Icons.LAPTOP_CHROMEBOOK,
            width=220, 
            on_click= lambda _:equipment_page(page),
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT:"#F0F0F8", ft.ControlState.HOVERED:"#778FD2"},
                animation_duration=200,
                shape={ft.ControlState.DEFAULT:ft.RoundedRectangleBorder(3), ft.ControlState.HOVERED: ft.RoundedRectangleBorder(20)},
                icon_color={ft.ControlState.DEFAULT: "0d1611", ft.ControlState.HOVERED: "#ffffff"},
                color={ft.ControlState.DEFAULT: "0d1611", ft.ControlState.HOVERED: "#ffffff"}))
        cabinetsButton=ft.ElevatedButton(
            "Кабинеты", 
            on_click=lambda _:cabinets_page(page),
            width=220, 
            icon=ft.Icons.ROOM,
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT:"#F0F0F8", ft.ControlState.HOVERED:"#778FD2"},
                animation_duration=200,
                shape={ft.ControlState.DEFAULT:ft.RoundedRectangleBorder(3), ft.ControlState.HOVERED: ft.RoundedRectangleBorder(20)},
                icon_color={ft.ControlState.DEFAULT: "0d1611", ft.ControlState.HOVERED: "#ffffff"},
                color={ft.ControlState.DEFAULT: "0d1611", ft.ControlState.HOVERED: "#ffffff"}))
        equipmentStatusButton=ft.ElevatedButton(
            "Статус оборудования", 
            on_click=lambda _: equipmentStatus_page(page),
            width=220, 
            icon=ft.Icons.ARCHIVE,
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT:"#F0F0F8", ft.ControlState.HOVERED:"#778FD2"},
                animation_duration=200,
                shape={ft.ControlState.DEFAULT:ft.RoundedRectangleBorder(3), ft.ControlState.HOVERED: ft.RoundedRectangleBorder(20)},
                icon_color={ft.ControlState.DEFAULT: "0d1611", ft.ControlState.HOVERED: "#ffffff"},
                color={ft.ControlState.DEFAULT: "0d1611", ft.ControlState.HOVERED: "#ffffff"}))
        equipmentCategoryButton=ft.ElevatedButton(
            "Категории оборудования", 
            on_click=lambda _:equipmentCategory_page(page),
            width=220, 
            icon=ft.Icons.SEGMENT,
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT:"#F0F0F8", ft.ControlState.HOVERED:"#778FD2"},
                animation_duration=200,
                shape={ft.ControlState.DEFAULT:ft.RoundedRectangleBorder(3), ft.ControlState.HOVERED: ft.RoundedRectangleBorder(20)},
                icon_color={ft.ControlState.DEFAULT: "0d1611", ft.ControlState.HOVERED: "#ffffff"},
                color={ft.ControlState.DEFAULT: "0d1611", ft.ControlState.HOVERED: "#ffffff"}))
        manageAdminAccButton=ft.ElevatedButton(
            "Администраторы", 
            icon=ft.Icons.VERIFIED_USER,
            on_click=lambda _: manageAdminAcc_page(page),
            width=220,
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT:"#F0F0F8", ft.ControlState.HOVERED:"#778FD2"},
                animation_duration=200,
                shape={ft.ControlState.DEFAULT:ft.RoundedRectangleBorder(3), ft.ControlState.HOVERED: ft.RoundedRectangleBorder(20)},
                icon_color={ft.ControlState.DEFAULT: "0d1611", ft.ControlState.HOVERED: "#ffffff"},
                color={ft.ControlState.DEFAULT: "0d1611", ft.ControlState.HOVERED: "#ffffff"}))
        if(page.platform==ft.PagePlatform.WINDOWS):
            main_image=ft.Image("Desktop\\Image\\main_object_2.png", width=700,height=700) if(os.path.isdir("_internal")!=True) else ft.Image("_internal\\Image\\main_object_2.png", width=700,height=700)
        else:
            path=os.getcwd()
            main_image=ft.Image(path+"/Desktop/Image/main_object_2.png", width=700,height=700) if(os.path.isdir("_internal")!=True) else ft.Image(path+"/_internal/Image/main_object_2.png", width=700,height=700)
        
        page.add(ft.Row([
            main_image,
            ft.Column([
                ft.Text("",height=20),
                requestPageButton,
                equipmentPageButton,
                cabinetsButton,
                equipmentStatusButton,
                equipmentCategoryButton,
                manageAdminAccButton
            ])
            ], spacing=100, alignment=ft.MainAxisAlignment.CENTER))
        
        logger_pages.info("'Main' page was openned")
        page.window.center()
        page.update()
    except Exception as ex:
        logger_pages.error(ex)


def resetPassword_page(page: ft.Page):

    page.clean()

    information_Text_1=ft.Text("Забыли пароль?", size=30, selectable=False,weight=ft.FontWeight.BOLD,font_family="Main Label", text_align=ft.TextAlign.CENTER)
    information_Text_2=ft.Text("Для восстановления пароля нужно перейти в Telegram аккаунт, который зарегистрирован на данную машину", size=14, selectable=False,font_family="Moderustic Light",width=230,text_align=ft.TextAlign.CENTER)

    resetPasswButton=ft.ElevatedButton(
        "Сбросить пароль", 
        icon=ft.Icons.RESTART_ALT_OUTLINED,
        icon_color=ft.Colors.WHITE,
        bgcolor=deskU.ui_colors[1],
        color=ft.Colors.WHITE,
        on_click=lambda _:page.launch_url("https://t.me/HAMT_Tech_Bot?start=resetPassword"))

    errorLabel=ft.Text("", font_family="Moderustic Regular", size=13,disabled=True,height=30)

    backPageButton=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: start_page(page), visible=True, icon_color=deskU.ui_colors[1], splash_radius=10)

    page.add(
        ft.Row([backPageButton],alignment=ft.MainAxisAlignment.START),
        ft.Column([information_Text_1, information_Text_2], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Text("", height=20),
        resetPasswButton)
    logger_pages.info("'Reset password' page was openned")
    page.window.center()
    page.update()


def start_page(page:ft.Page):

    try:

        def nextPage(self):
            try:
                result=db_object.request_execute(f"Select * from Administrators where (Login='{(sha384(loginField.value.encode()).hexdigest())}' OR TG_Username='{(sha384(loginField.value.encode()).hexdigest())}') AND Password='{(sha384(passwordField.value.encode()).hexdigest())}'")
                if (result!=False):
                    if(len(result)!=0):
                        main_page_v2(page)
                    else:
                        deskU.errorField(self)
                else:
                    deskU.errorField(self)
            except Exception as ex:
                deskU.errorField(self)
                raise Exception(ex)

        def resetPassword(self):
            resetPassword_page(self.page)

        page.clean()


        page.window.width=800
        page.window.height=700

        page.title="НАМТ.Администраторы"
        path=os.getcwd()
        page.theme_mode=ft.ThemeMode.LIGHT
        page.vertical_alignment=ft.MainAxisAlignment.CENTER
        page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
        page.window.resizable=False
        page.window.prevent_close=True
        page.window.on_event=deskU.pageClose
        if(page.platform==ft.PagePlatform.WINDOWS):
            page.window.icon=path+"\\Desktop\\Image\\HAMT_Logo.ico" if (os.path.isdir("_internal")!=True) else path+'\\_internal\\Image\\HAMT_Logo.ico'
            page.fonts={
            'Main Label': 'Fonts\\TechMonoRegular.otf' if (os.path.isdir("_internal")!=True) else '_internal\\Fonts\\TechMonoRegular.otf',
            'Moderustic Bold': 'Fonts\\Moderustic\\Moderustic-Bold.ttf' if (os.path.isdir("_internal")!=True) else '_internal\\Fonts\\Moderustic\\Moderustic-Bold.ttf',
            'Moderustic Light':'Fonts\\Moderustic\\Moderustic-Light.ttf' if (os.path.isdir("_internal")!=True) else '_internal\\Fonts\\Moderustic\\Moderustic-Light.ttf',
            'Moderustic Regular':'Fonts\\Moderustic\\Moderustic-Regular.ttf' if (os.path.isdir("_internal")!=True) else '_internal\\Fonts\\Moderustic\\Moderustic-Regular.ttf'}
        else:
            page.window.icon=path+"/Desktop/Image/HAMT_Logo.ico" if (os.path.isdir("_internal")!=True) else path+'/_internal/Image/HAMT_Logo.ico'
            page.fonts={
            'Main Label': path+'/Fonts/TechMonoRegular.otf' if (os.path.isdir("_internal")!=True) else '_internal/Fonts/TechMonoRegular.otf',
            'Moderustic Bold': path+'/Fonts/Moderustic/Moderustic-Bold.ttf' if (os.path.isdir("_internal")!=True) else path+'/_internal/Fonts/Moderustic/Moderustic-Bold.ttf',
            'Moderustic Light':path+'/Fonts/Moderustic/Moderustic-Light.ttf' if (os.path.isdir("_internal")!=True) else path+'/_internal/Fonts/Moderustic/Moderustic-Light.ttf',
            'Moderustic Regular':path+'/Fonts/Moderustic/Moderustic-Regular.ttf' if (os.path.isdir("_internal")!=True) else path+'/_internal/Fonts/Moderustic/Moderustic-Regular.ttf'}


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
            color=ft.Colors.WHITE)
        
        resetPasswordButton=ft.ElevatedButton("Забыли пароль?", width=150, on_click=resetPassword, bgcolor=ft.Colors.WHITE)
        registrPasswordButton=ft.ElevatedButton("Регистрация", width=150, on_click=lambda _:startAdmin_page(page), bgcolor="#8FA2CA",color=ft.Colors.WHITE)

        page.add(ft.Column([startLabel,startDescriptionLabel],spacing=5,horizontal_alignment=ft.CrossAxisAlignment.CENTER),ft.Text("",height=30),loginField,passwordField,enterButton,ft.Text("",height=20),ft.Row([registrPasswordButton,resetPasswordButton],spacing=15,alignment=ft.MainAxisAlignment.CENTER))
        
        if(os.path.isfile("Admin Configure")==True):

            with open("Admin Configure", 'r') as File:
                line=File.readlines()
                if (len(line)!=0):
                    if (line[0]=="Enter Today:1"):
                        startDescriptionLabel.value=deskU.login_coLabelText[randint(0,len(deskU.login_coLabelText)-1)]
                    elif (line[0]!=f"Enter Today:{datetime.datetime.now().strftime('%D')}"):
                        startDescriptionLabel.value=deskU.login_coLabelText[2]
                    else:
                        startDescriptionLabel.value=deskU.login_coLabelText[1]
                else:
                    startDescriptionLabel.value="Вы здесь в первый раз?\nДля дальнейшей работы вам необходимо зарегистрироваться или войти в аккаунт"


        else:

            startDescriptionLabel.value="Вы здесь в первый раз?\nДля дальнейшей работы вам необходимо зарегистрироваться или войти в аккаунт"
            registrPasswordButton.focus()

        logger_pages.info("'Start' page was openned")
        page.window.center()
        page.update()
    except Exception as ex:
        raise Exception(ex)


def startAdmin_page(page:ft.Page):

    def backPage(self):

        start_page(self.page)

    def adminRegInBD(self):

        if (failedRegistLabel.value!=""):
            failedRegistLabel.value=""


        result=db_object.request_execute(f"Select * from Administrators where TG_Username='{sha384(usernameField.value.encode()).hexdigest()}' OR FSL='{(fslField.value)}' OR Mac_Address='{hex(uuid.getnode())}'")

        if((fslField.value!="" and len(fslField.value.split(" "))==3) and (loginField.value!="" and len(loginField.value)<=255) and (usernameField.value!="" and usernameField.value.find("@")==-1) and (passwordField.value!="" and len(passwordField.value)>=3)):

            if (result!=False):
                if (len(result)==0):

                    result=db_object.request_execute(f"Insert into Administrators(FSL,Login, Mac_Address,Password, TG_Username) values ('{(fslField.value)}', '{sha384(loginField.value.encode()).hexdigest()}', '{hex(uuid.getnode())}' ,'{sha384(passwordField.value.encode()).hexdigest()}', '{sha384(usernameField.value.encode()).hexdigest()}')")
                    if (result!=False):
                        with open("Admin Configure", 'w') as bFile:
                            bFile.write(f"Enter Today: 1")

                        for i in range(1,len(self.page.controls)):
                            self.page.controls[i].disabled=True
                        
                        deskU.successField(self)

                    else:

                        deskU.errorField(self)

                else:
                    failedRegistLabel.value="Аккаут с такими данными уже зарегистрирован или данное устройство уже\nнаходится в базе данных приложения"
                    deskU.errorField(self)
                
                    self.page.update()
            else:
                page.window.bgcolor=ft.Colors.RED_300
                failedRegistLabel.value="Ошибка выполнения запроса\nВозможно неверно заполненные данные"

                self.page.update()
                time.sleep(0.7)

                page.window.bgcolor=ft.Colors.TRANSPARENT
                self.page.update()

        else:
            baseColor=self.page.controls[3].border_color
            deskU.checkFieldOnIncosist(self,0)

            if (page.controls[6].border_color!=ft.Colors.RED):
                page.controls[6].border_color=ft.Colors.RED
                page.update()

            time.sleep(0.7)

        for control in self.page.controls:
                if (type(control)==ft.TextField):
                    control.border_color=baseColor
        self.page.update()
            

    page.clean()

    page.window.width=800
    page.window.height=700

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
        can_reveal_password=True,
        hint_style=ft.TextStyle(font_family="Moderustic Regular"),
        border_radius=14, 
        max_lines=1, 
        border_color=deskU.ui_colors[0],
        on_focus=deskU.contentColor_focus,
        on_blur=deskU.contentColor_blur)
    
    failedRegistLabel=ft.Text("", font_family="Moderustic Regular",size=13,width=200)

    regirtrAdminButton=ft.ElevatedButton("Зарегистрироваться", width=165, on_click=adminRegInBD, bgcolor=deskU.ui_colors[1],color=ft.Colors.WHITE)
    password_generate_button=ft.IconButton(ft.Icons.PASSWORD, on_click=deskU.password_generator, icon_color=deskU.ui_colors[1], tooltip="Генерация пароля")
    backPageButton=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=backPage, icon_color=deskU.ui_colors[1], splash_radius=10)

    page.add(
        ft.Row([backPageButton], alignment=ft.MainAxisAlignment.START),
        ft.Column([startLabel,startDescriptionLabel],spacing=5),
        ft.Text("",height=30) ,
        fslField,loginField,usernameField,ft.Row([ft.Text("", width=22),passwordField,password_generate_button], spacing=10,alignment=ft.MainAxisAlignment.CENTER , width=275),
        failedRegistLabel,
        ft.Text("",height=30),
        regirtrAdminButton)
    logger_pages.info("'StartAdmin' page was openned")
    page.window.center()
    page.update()