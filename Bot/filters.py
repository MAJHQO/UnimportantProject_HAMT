from aiogram import Bot
from aiogram.types import  Message, ChatMemberAdministrator, ChatMemberMember, ChatMemberOwner,CallbackQuery
from aiogram.filters import BaseFilter, CommandObject
from hashlib import sha384

from utilits.bd import db_object

import Bot.bot_config as bot_config

MemberStatus = [ChatMemberMember, ChatMemberOwner, ChatMemberAdministrator]

class teacherFilter_Call(BaseFilter):

    async def __call__(self, callback: CallbackQuery, bot: Bot) -> bool:
        if (not callback.from_user): 
            return False
        
        result=db_object.request_execute("Select TG_ID from Users")

        chc=False

        if (len(result)!=0):

            for i in result:
                if (sha384(str(callback.from_user.id).encode()).hexdigest() in i):

                    chc=True
                        
                    break

        if (chc==False):

            db_object.request_execute(f"Insert into Users(TG_ID, Username,FSL) values ('{sha384(str(callback.from_user.id).encode()).hexdigest()}', '{sha384(callback.from_user.username.encode()).hexdigest}','-')")

            
        del result,chc
            
        return type(await bot.get_chat_member(bot_config.teacher_chatID, callback.from_user.id)) in MemberStatus and callback.message.chat.type!='supergroup'
        
class teacherFilter(BaseFilter):

    async def __call__(self, message: Message, bot: Bot) -> bool:
        if (not message.from_user): 
            return False
        
        result=db_object.request_execute("Select TG_ID from Users")

        chc=False

        if (len(result)!=0):

            for i in result:
                if (sha384(str(message.from_user.id).encode()).hexdigest() in i):

                    chc=True
                        
                    break

        if (chc==False):

            db_object.request_execute(f"Insert into Users(TG_ID, Username,FSL) values ('{sha384(str(message.from_user.id).encode()).hexdigest()}', '{sha384(message.from_user.username.encode()).hexdigest}','-')")

            
        del result,chc
            
        return type(await bot.get_chat_member(bot_config.teacher_chatID, message.from_user.id)) in MemberStatus and message.chat.type!='supergroup'