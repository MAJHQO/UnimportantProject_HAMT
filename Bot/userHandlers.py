from aiogram import types, Router
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,KeyboardButton,FSInputFile,URLInputFile,InputFile
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.enums import ParseMode, ChatAction
from aiogram import F

from inspect import currentframe, getframeinfo
from hashlib import sha384

import bot_main as main
from utilits import utilits_desktop as ut
from utilits.bd import db_object
from Bot.filters import teacherFilter,teacherFilter_Call

import Bot.FSM as FSM ,Bot.keyboards as keyboards,Bot.bot_config as bConfig

router = Router()

router.message.filter(teacherFilter())
router.callback_query.filter(teacherFilter_Call())

keyboard=ReplyKeyboardBuilder()

@router.message(CommandStart())
async def start(message:types.Message, command: CommandObject, state: FSMContext):
    
    frameinfo = getframeinfo(currentframe())

    main.logger.info(f' UserID/Username: {message.from_user.id}/{message.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno}')

    try:

        await state.set_state(None)

        if (command.args!=None):
            if(command.args=='resetPassword'):
                if (len(db_object.request_execute(f"Select * from Administrators where TG_Username='{sha384(message.from_user.username.encode()).hexdigest()}'"))!=0):
                    await message.answer("Введите новый пароль: ")
                    await state.set_state(FSM.Password_Reset.password)
        else:
            result=db_object.request_execute(f"Select * from Users where TG_ID={message.from_user.id} AND FSL!='-'")
            if (result!=False and len(result)==0):
                await message.answer(bConfig.startText, parse_mode=ParseMode.HTML , reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Регистрация", callback_data="User_Registration")]]))
            else:
                await message.answer("Главное меню", reply_markup=keyboards.mainKeyboard)
                
    except Exception as ex:

        frameinfo = getframeinfo(currentframe())

        main.logger.error(f' UserID/Username: {message.from_user.id}/{message.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno} | Text: {ex}')
                

@router.callback_query(F.data=="User_Registration")
async def User_Registration(callback:types.CallbackQuery, state: FSMContext):
    
    frameinfo = getframeinfo(currentframe())

    main.logger.info(f' UserID/Username: {callback.from_user.id}/{callback.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno}')

    try:

        await callback.message.edit_text("Введите Ваше ФИО")

        await state.set_state(FSM.User_Registration.FSL_name)

    except Exception as ex:

        frameinfo = getframeinfo(currentframe())

        main.logger.error(f' UserID/Username: {callback.from_user.id}/{callback.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno} | Text: {ex}')


@router.callback_query(F.data.startswith("Back_Scenario"))
async def back_scenario_handler(callback:types.CallbackQuery, state: FSMContext):

    frameinfo = getframeinfo(currentframe())

    main.logger.info(f' UserID/Username: {callback.from_user.id}/{callback.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno}')

    try:

        if(callback.data.split("_")[2]=="0"):
            result=f"Select * from Users where TG_ID={callback.from_user.id} AND FSL!='-'"
            if (result!=False and len(result)==0):
                await callback.message.edit_text(bConfig.startText, parse_mode=ParseMode.HTML , reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Регистрация", callback_data="User_Registration")]]))
            else:
                await callback.message.edit_text("Главное меню", reply_markup=keyboards.mainKeyboard)

        elif(callback.data.split("_")[2]=="1"):

            await callback.message.edit_text("Введите Ваше ФИО")

            await state.set_state(FSM.User_Registration.FSL_name)

        elif (callback.data.split("_")[2]=="2"):

            await callback.message.edit_text(f"Аккаунт: {db_object.request_execute(f'Select FSL from Users where TG_ID={callback.from_user.id}')[0][0]}",reply_markup=keyboards.accountKeyboard)

        elif(callback.data.split("_")[2]=="3"):

            await callback.message.edit_text("Введите Ваше ФИО")

            await state.set_state(FSM.User_Registration.FSL_Rename)

        elif(callback.data.split("_")[2]=="4"):

            await account(callback)

    except Exception as ex:

        frameinfo = getframeinfo(currentframe())

        main.logger.error(f' UserID/Username: {callback.from_user.id}/{callback.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno} | Text: {ex}')


@router.callback_query(F.data.startswith("New_Request"))
async def new_request(callback:types.CallbackQuery, state: FSMContext):
    
    frameinfo = getframeinfo(currentframe())

    main.logger.info(f' UserID/Username: {callback.from_user.id}/{callback.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno}')

    try:

       await callback.message.edit_text("Введите номер кабинета, к которому будет прикреплена данная заявка",reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад",callback_data="Back_Scenario_0")]]))

       await state.set_state(FSM.New_Request.Cabinet_Number)

    except Exception as ex:

        frameinfo = getframeinfo(currentframe())

        main.logger.error(f' UserID/Username: {callback.from_user.id}/{callback.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno} | Text: {ex}')


@router.callback_query(F.data=="User_Account")
async def account(callback:types.CallbackQuery):

    frameinfo = getframeinfo(currentframe())

    main.logger.info(f' UserID/Username: {callback.from_user.id}/{callback.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno}')

    try:
        await callback.message.edit_text(f"Аккаунт: {db_object.request_execute(f'Select FSL from Users where TG_ID={callback.from_user.id}')[0][0]}",reply_markup=keyboards.accountKeyboard)

    except Exception as ex:

        frameinfo = getframeinfo(currentframe())

        main.logger.error(f' UserID/Username: {callback.from_user.id}/{callback.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno} | Text: {ex}')


@router.callback_query(F.data=="View_Own_Request")
async def view_request(callback:types.CallbackQuery):
    
    frameinfo = getframeinfo(currentframe())

    main.logger.info(f' UserID/Username: {callback.from_user.id}/{callback.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno}')

    try:

        result=db_object.request_execute(f"Select Cabinet_Number, Request_Description,Request_Status from Repair_Request where TG_ID={callback.from_user.id}")
        toUserMessage=""
        inKeyboard=keyboards.backButton
        inKeyboard.inline_keyboard[0][0].callback_data='Back_Scenario_2'

        for i in result:
            toUserMessage+=f"Кабинет: {i[0]} - Статус: {i[2]}\nОписание: {i[1]}\n\n"

        if (len(toUserMessage)>4096):
            await callback.message.edit_text(toUserMessage[:len(toUserMessage)])
            await callback.message.answer(toUserMessage[len(toUserMessage)+1:], reply_markup=inKeyboard)
        elif(len(toUserMessage)==0):
            await callback.message.edit_text("На данный момент - у вас не имеется активных заявок", reply_markup=inKeyboard)
        else:
            await callback.message.edit_text(toUserMessage,reply_markup=inKeyboard)

    except Exception as ex:

        frameinfo = getframeinfo(currentframe())

        main.logger.error(f' UserID/Username: {callback.from_user.id}/{callback.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno} | Text: {ex}')


@router.callback_query(F.data=="Change_User_FSL")
async def view_request(callback:types.CallbackQuery, state:FSMContext):
    
    frameinfo = getframeinfo(currentframe())

    main.logger.info(f' UserID/Username: {callback.from_user.id}/{callback.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno}')

    try:

        await callback.message.edit_text("Введите ваше ФИО")
        await state.set_state(FSM.User_Registration.FSL_Rename)

    except Exception as ex:

        frameinfo = getframeinfo(currentframe())

        main.logger.error(f' UserID/Username: {callback.from_user.id}/{callback.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno} | Text: {ex}')



@router.message(FSM.User_Registration.FSL_name)
async def User_Registration_name(message:types.Message, state: FSMContext):
    
    frameinfo = getframeinfo(currentframe())

    main.logger.info(f' UserID/Username: {message.from_user.id}/{message.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno}')

    try:
       
        if (len(message.text.split(" "))==3):

            await state.update_data(FSL_name=message.text)
            data=await state.get_data()
        
            result=db_object.request_execute(f"Update Users Set FSL='{data['FSL_name']}' where TG_ID={message.from_user.id}")

            if (result!=False):

                await message.answer("Регистрация выполнена успешно")
                await message.answer("Главное меню", reply_markup=keyboards.mainKeyboard)
            else:
                await message.answer("При выполнении регистрации возникла ошибка", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Повторить",callback_data="Back_Scenario_1")], 
                    [InlineKeyboardButton(text="Назад",callback_data="Back_Scenario_0")]]))

        else:

            inKeyboard=keyboards.backButton
            inKeyboard.inline_keyboard[0][0].callback_data='Back_Scenario_1'
           
            await message.answer("Данное сообщение не явлется соответствующим ФИО, т.к не содержит нужного количества частей.\n\nВведите Ваше ФИО",reply_markup=inKeyboard)

            await state.set_state(FSM.User_Registration.FSL_name)

            frameinfo = getframeinfo(currentframe())

            main.logger.exception(f' UserID/Username: {message.from_user.id}/{message.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno} | Text: Недостаточное количество слов для ФИО')

    except Exception as ex:

        frameinfo = getframeinfo(currentframe())

        main.logger.error(f' UserID/Username: {message.from_user.id}/{message.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno} | Text: {ex}')


@router.message(FSM.New_Request.Cabinet_Number)
async def New_Request_CN(message:types.Message, state: FSMContext):
    
    frameinfo = getframeinfo(currentframe())

    main.logger.info(f' UserID/Username: {message.from_user.id}/{message.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno}')

    try:
        result=db_object.request_execute(f"Select * from Cabinets where Number='{message.text}'")
        if (message.text.isdigit()==True and result!=False and len(result)>0):
            await state.update_data(Cabinet_Number=int(message.text))
            await message.answer("Введите описание заявки")
            await state.set_state(FSM.New_Request.Request_Description)
        else:
            await message.answer("Данное сообщение не является подходящим по формату или же данного кабинета не существует\n\nНомер кабинета должен быть целым числом")
            await message.answer("Введите номер кабинета, к которому будет прикреплена данная заявка", reply_markup=keyboards.backButton)

            await state.set_state(FSM.New_Request.Cabinet_Number)

    except Exception as ex:

        frameinfo = getframeinfo(currentframe())

        main.logger.error(f' UserID/Username: {message.from_user.id}/{message.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno} | Text: {ex}')

        await message.answer("При выполнении программы возникла ошибка\n\nВведите Ваше ФИО", reply_markup=keyboards.backButton)

        await state.set_state(FSM.New_Request.Cabinet_Number)

@router.message(FSM.New_Request.Request_Description)
async def New_Request_CN(message:types.Message, state: FSMContext):
    
    frameinfo = getframeinfo(currentframe())

    main.logger.info(f' UserID/Username: {message.from_user.id}/{message.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno}')

    try:
       
        await state.update_data(Request_Description=message.text)
        data=await state.get_data()
        result=db_object.request_execute(f"Insert into Repair_Request(Request_Number,TG_ID,TG_Username,Cabinet_Number,Request_Description,Request_Status) values((Select COUNT(*) as count from Repair_Request)+1, {message.from_user.id}, '{message.from_user.username}', {data['Cabinet_Number']}, '{data['Request_Description']}', '-')")
        
        if(result!=False):
        
            await message.answer("Заявка успешно сформирована", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Новая заявка", callback_data="New_Request")],
                [InlineKeyboardButton(text="Назад", callback_data="Back_Scenario_0")]]))
            
        else:

            await message.answer("При выполнении программы возникла ошибка\n\nВведите описание заявки", reply_markup=keyboards.backButton)
            await state.set_state(FSM.New_Request.Request_Description)

    except Exception as ex:

        frameinfo = getframeinfo(currentframe())

        main.logger.error(f' UserID/Username: {message.from_user.id}/{message.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno} | Text: {ex}')

        await message.answer("При выполнении программы возникла ошибка\n\nВведите описание заявки", reply_markup=keyboards.backButton)
        await state.set_state(FSM.New_Request.Request_Description)

@router.message(FSM.User_Registration.FSL_Rename)
async def user_rename(message:types.Message, state: FSMContext):
    frameinfo = getframeinfo(currentframe())

    main.logger.info(f' UserID/Username: {message.from_user.id}/{message.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno}')

    try:
       
        if (len(message.text.split(" "))==3):

            await state.update_data(FSL_name=message.text)
            data=await state.get_data()
        
            result=db_object.request_execute(f"Update Users Set FSL='{data['FSL_name']}' where TG_ID={message.from_user.id}")

            if (result!=False):

                await message.answer("Изменение выполнено успешно")
                await message.answer("Главное меню", reply_markup=keyboards.mainKeyboard)
            else:
                await message.answer("При выполнении изменения возникла ошибка", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Повторить",callback_data="Back_Scenario_3")], 
                    [InlineKeyboardButton(text="Назад",callback_data="Back_Scenario_0")]]))

        else:

            inKeyboard=keyboards.backButton
            inKeyboard.inline_keyboard[0][0].callback_data='Back_Scenario_4'
           
            await message.answer("Данное сообщение не явлется соответствующим ФИО, т.к не содержит нужного количества частей.\n\nВведите Ваше ФИО",reply_markup=inKeyboard)

            await state.set_state(FSM.User_Registration.FSL_Rename)

            frameinfo = getframeinfo(currentframe())

            main.logger.exception(f' UserID/Username: {message.from_user.id}/{message.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno} | Text: Недостаточное количество слов для ФИО')

    except Exception as ex:

        frameinfo = getframeinfo(currentframe())

        main.logger.error(f' UserID/Username: {message.from_user.id}/{message.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno} | Text: {ex}')

@router.message(FSM.Password_Reset.password)
async def user_rename(message:types.Message, state: FSMContext):
    frameinfo = getframeinfo(currentframe())

    main.logger.info(f' UserID/Username: {message.from_user.id}/{message.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno}')

    try:
        db_object.request_execute(f"Update Administrators Set Password='{sha384(message.text.encode()).hexdigest()}' where TG_Username='{sha384(message.from_user.username.encode()).hexdigest()}'")
    except Exception as ex:

        frameinfo = getframeinfo(currentframe())

        main.logger.error(f' UserID/Username: {message.from_user.id}/{message.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno} | Text: {ex}')