from aiogram import Bot
from aiogram.types import  Message, ChatMemberAdministrator, ChatMemberMember, ChatMemberOwner,CallbackQuery
from aiogram.filters import BaseFilter, CommandObject

from ..utilits import bd

import config, numpy

MemberStatus = [ChatMemberMember, ChatMemberOwner, ChatMemberAdministrator]

class BaseFilter(BaseFilter):

    async def __call__(self, message: Message, bot: Bot) -> bool:
        if (not message.from_user): 
            return False