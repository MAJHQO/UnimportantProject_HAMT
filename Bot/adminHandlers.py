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

router = Router()

router.message.filter(BannedUser())
router.callback_query.filter(BannedUser_Call())

keyboard=ReplyKeyboardBuilder()