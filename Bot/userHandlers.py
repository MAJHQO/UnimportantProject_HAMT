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

from .. import bot_main as main
from ..utilits import bd

router = Router()

# router.message.filter(BannedUser())
# router.callback_query.filter(BannedUser_Call())

keyboard=ReplyKeyboardBuilder()

@router.message(CommandStart())
async def start(message:types.Message, command: CommandObject, state: FSMContext):
    
    frameinfo = getframeinfo(currentframe())

    main.logger.info(f' UserID/Username: {message.from_user.id}/{message.from_user.username} | Event: {__file__} | Line: {frameinfo.lineno}')

    await state.set_state(None)

    if (command.args!=None):
        pass
    else:
        if (len(bd.reqExecute(f"Select * from Users where TG_ID={message.from_user.id}"))==0):
            message.answer("Здравствуйте! Данный бот предназначен для формирования заявки на исправление проблемы | починку | замену оборудования в данном учебном учреждении", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Регистрация")]]))
        else:
            pass