from aiogram import Bot
from aiogram.types import  Message, ChatMemberAdministrator, ChatMemberMember, ChatMemberOwner,CallbackQuery
from aiogram.filters import BaseFilter, CommandObject

from utilits import bd

import Bot.bot_config as bot_config

MemberStatus = [ChatMemberMember, ChatMemberOwner, ChatMemberAdministrator]

class teacherFilter_Call(BaseFilter):

    async def __call__(self, callback: CallbackQuery, bot: Bot) -> bool:
        if (not callback.from_user): 
            return False
        
        result=bd.reqExecute("Select TG_ID from Users")

        chc=False

        if (len(result)!=0):

            for i in result:
                if (callback.from_user.id == i[0]):

                    chc=True
                        
                    break

        if (chc==False):

            bd.reqExecute(f"Insert into Users(TG_ID, Username,FSL) values ({callback.from_user.id }, '{callback.from_user.username}','-')")

            
        del result,chc
            
        return type(await bot.get_chat_member(bot_config.teacher_chatID, callback.from_user.id)) in MemberStatus and callback.message.chat.type!='supergroup'
        
class teacherFilter(BaseFilter):

    async def __call__(self, message: Message, bot: Bot) -> bool:
        if (not message.from_user): 
            return False
        
        result=bd.reqExecute("Select TG_ID from Users")

        chc=False

        if (len(result)!=0):

            for i in result:
                if (message.from_user.id in i):

                    chc=True
                        
                    break

        if (chc==False):

            bd.reqExecute(f"Insert into Users(TG_ID, Username,FSL) values ({message.from_user.id }, '{message.from_user.username}','-')")

            
        del result,chc
            
        return type(await bot.get_chat_member(bot_config.teacher_chatID, message.from_user.id)) in MemberStatus and message.chat.type!='supergroup'