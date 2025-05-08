from aiogram.fsm.state import State, StatesGroup

class User_Registration(StatesGroup):
    FSL_name=State()
    FSL_Rename=State()

class New_Request(StatesGroup):
    Cabinet_Number=State()
    Request_Description=State()
    Request_Status=State()
