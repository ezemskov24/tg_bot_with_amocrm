from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    amount = State()
    term = State()
    contract_type = State()
    participation_type = State()
    advance = State()
    dept = State()
    urgency = State()
    comment = State()
    request_phone = State()
    last = State()