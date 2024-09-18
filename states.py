from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    amount = State()
    term = State()
    contract_type = State()
    participation_type = State()
    advance = State()
    proceeds = State()
    dept = State()
    urgency = State()
    comment = State()
    name = State()
    request_phone = State()
    last = State()