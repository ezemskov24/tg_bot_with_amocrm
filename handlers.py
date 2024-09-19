from datetime import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, \
    InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command

from states import Form
from amo_integration import add_deal, Person

router = Router()

@router.message(Command('start'))
async def start_handler(msg: Message, state: FSMContext):
    await msg.answer('Вас приветствует бот команды БанкГарант24\n'
                     '\n'
                     'Введите Ваше имя')
    await state.set_state(Form.amount)


@router.message(Form.amount)
async def amount_handler(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer('Введите сумму банковской гарантии в рублях.\n'
                 'Поле должно содержать только цифры, без пробелов.')
    await state.set_state(Form.term)


@router.message(Form.term)
async def term_handler(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer('Поле должно содержать только цифры. Повторите ввод')
        return
    else:
        await state.update_data(amount=msg.text)
        await msg.answer('Введите срок банковской гарантии (в месяцах)')
        await state.set_state(Form.contract_type)


@router.message(Form.contract_type)
async def check_contract_type(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer('Поле должно содержать только цифры. Повторите ввод')
        return
    else:
        await state.update_data(term=msg.text)
        keyboard_builder = InlineKeyboardBuilder()
        keyboard_builder.row(
            InlineKeyboardButton(text='44 Федеральный закон', callback_data='44 Федеральный закон')
        )
        keyboard_builder.row(
            InlineKeyboardButton(text='223 Федеральный закон', callback_data='223 Федеральный закон')
        )
        keyboard_builder.row(
            InlineKeyboardButton(text='Коммерческий контракт', callback_data='Коммерческий контракт')
        )
        keyboard_builder.row(
            InlineKeyboardButton(text='Другое', callback_data='Другое')
        )
        await msg.answer('Выберите тип контракта', reply_markup=keyboard_builder.as_markup())


@router.callback_query(lambda c: c.data in ['44 Федеральный закон', '223 Федеральный закон', 'Коммерческий контракт', 'Другое'])
async def contract_type_callback(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(contract_type=callback_query.data)
    if callback_query.data == '44 Федеральный закон':
        await callback_query.message.answer('Вы выбрали: 44 ФЗ')
    elif callback_query.data == '223 Федеральный закон':
        await callback_query.message.answer('Вы выбрали: 223 ФЗ')
    elif callback_query.data == 'Коммерческий контракт':
        await callback_query.message.answer('Вы выбрали: Коммерческий контракт')
    elif callback_query.data == 'Другое':
        await callback_query.message.answer('Вы выбрали: Другое')

    await state.set_state(Form.participation_type)
    await check_participation_type(callback_query.message, state)


@router.message(Form.participation_type)
async def check_participation_type(msg: Message, state: FSMContext):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(text='На исполнение контракта', callback_data='На исполнение контракта')
    )
    keyboard_builder.row(
        InlineKeyboardButton(text='На участие', callback_data='На участие')
    )
    keyboard_builder.row(
        InlineKeyboardButton(text='Другое', callback_data='Другое ')
    )
    await msg.answer(text='Гарантия требуется на исполнение контракта или на участие?', reply_markup=keyboard_builder.as_markup())


@router.callback_query(lambda c: c.data in ['На исполнение контракта', 'На участие', 'Другое '])
async def participation_type_callback(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(participation_type=callback_query.data)
    if callback_query.data == 'На исполнение контракта':
        await callback_query.message.answer('Вы выбрали: На исполнение контракта')
    elif callback_query.data == 'На участие':
        await callback_query.message.answer('Вы выбрали: На участие')
    elif callback_query.data == 'Другое ':
        await callback_query.message.answer('Вы выбрали: Другое')

    await state.set_state(Form.advance)
    await check_advanced_payment(callback_query.message, state)


@router.message(Form.advance)
async def check_advanced_payment(msg: Message, state: FSMContext):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(text='Аванса нет', callback_data='Аванса нет')
    )
    keyboard_builder.row(
        InlineKeyboardButton(text='Аванс есть', callback_data='Аванс есть')
    )

    await msg.answer(text='Предусмотрено авансирование?', reply_markup=keyboard_builder.as_markup())


@router.callback_query(lambda c: c.data in ['Аванса нет', 'Аванс есть'])
async def advanced_payment_callback(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(advanced_payment=callback_query.data)
    if callback_query.data == 'Аванса нет':
        await callback_query.message.answer('Вы выбрали: Аванса нет')
    elif callback_query.data == 'Аванс есть':
        await callback_query.message.answer('Вы выбрали: Аванс есть')

    await state.set_state(Form.dept)
    await check_overdue_debt(callback_query.message, state)


@router.message(Form.dept)
async def check_overdue_debt(msg: Message, state: FSMContext):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(text='Да', callback_data='Да')
    )
    keyboard_builder.row(
        InlineKeyboardButton(text='Нет', callback_data='Нет')
    )
    await msg.answer(text='У вас есть просроченная задолженность?', reply_markup=keyboard_builder.as_markup())



@router.callback_query(lambda c: c.data in ['Да', 'Нет'])
async def overdue_debt_callback(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(overdue_debt=callback_query.data)
    if callback_query.data == 'Да':
        await callback_query.message.answer('Вы выбрали: Да')
    elif callback_query.data == 'Нет':
        await callback_query.message.answer('Вы выбрали: Нет')

    await state.set_state(Form.urgency)
    await check_urgency(callback_query.message, state)


@router.message(Form.urgency)
async def check_urgency(msg: Message, state: FSMContext):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(text='Срочно', callback_data='Срочно')
    )
    keyboard_builder.row(
        InlineKeyboardButton(text='Не срочно', callback_data='Не срочно')
    )
    await msg.answer(text='Как срочно нужна банковская гарантия?', reply_markup=keyboard_builder.as_markup())


@router.callback_query(lambda c: c.data in ['Срочно', 'Не срочно'])
async def urgency_callback(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(urgency=callback_query.data)
    if callback_query.data == 'Срочно':
        await callback_query.message.answer('Вы выбрали: Срочно')
    elif callback_query.data == 'Не срочно':
        await callback_query.message.answer('Вы выбрали: Не срочно')

    await state.set_state(Form.comment)
    await add_comment(callback_query.message, state)


@router.message(Form.comment)
async def add_comment(msg: Message, state: FSMContext):
    await msg.answer('Если у Вас есть дополнительные комментарии, можете написать здесь.\n'
                     'Либо отправить любой символ для перехода к следующему пункту.')

    await state.set_state(Form.request_phone)


@router.message(Form.request_phone)
async def add_phone(msg: Message, state: FSMContext):
    await state.update_data(comment=msg.text)

    phone_button = InlineKeyboardButton(text="Отправить номер телефона", callback_data="request_phone")
    phone_markup = InlineKeyboardMarkup(inline_keyboard=[[phone_button]])

    await msg.answer("Для продолжения, пожалуйста, отправьте ваш номер телефона:",
                                        reply_markup=phone_markup)



@router.callback_query(lambda c: c.data == 'request_phone')
async def request_phone_callback(callback_query: CallbackQuery, state: FSMContext):
    contact_button = KeyboardButton(text='Отправить номер телефона', request_contact=True)
    contact_markup = ReplyKeyboardMarkup(
        keyboard=[[contact_button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await callback_query.message.answer("Пожалуйста, отправьте ваш номер телефона:", reply_markup=contact_markup)
    await state.set_state(Form.last)


@router.message(Form.last)
async def last_handler(msg: Message, state: FSMContext):
    if msg.contact:
        contact = msg.contact.phone_number
        await state.update_data(contact=contact)
        data = await state.get_data()

        if int(data['amount']) <= 1000000:
            document_request = \
                (
                    f"1. Паспорт.\n"
                    f"2. Карточка с реквизитами.\n"
                    f"3. Номер аукциона. Если коммерческий контракт, то макет контракта.\n"
                )
        else:
            document_request = \
                (
                    f"1. Устав\n"
                    f"2. Решение на ген. директора\n"
                    f"3. Паспорта учредителей и директора.\n"
                    f"4. Карточка организации, договор аренды.\n"
                    f"5. Баланс 2023 с квитанцией о приеме и за первое полугодие 2024 года.\n"
                    f"6. Номер аукциона. Если коммерческий контракт, то макет контракта."
                )

        text_for_amo = (
            f"Имя: {data['name']}\n"
            f"Сумма банковской гарантии: {data['amount']} руб.\n"
            f"Срок банковской гарантии: {data['term']} мес.\n"
            f"Тип контракта: {data['contract_type']}\n"
            f"Этап сделки: {data['participation_type']}\n"
            f"Аванс: {data['advanced_payment']}\n"
            f"Задолженность: {data['overdue_debt']}\n"
            f"Срочность: {data['urgency']}\n"
            f"Комментарий: {data['comment']}\n"
            f"Номер телефона: {contact}\n"
        )

        response = (
            f"{text_for_amo}"
            f"\n"
            f"Наш менеджер свяжется с Вами в ближайшее время.\n"
            f"Чтобы ускорить процесс расчета, можете прислать документы из списка на электронную почту call-center@bankgarant24.ru\n"
            f"\n"
            f"Необходимые документы:\n"
            f"{document_request}"
        )

        await msg.answer(response)

        person = Person(first_name=data["name"], contact_phone=contact)
        add_deal(
            lead_name=f'БГ из Telegram на {data["amount"]}',
            user_id=10698318,
            status=64421054,
            person=person,
            task_text=text_for_amo,
            task_date=datetime.utcnow(),
            tags=["From Telegram"]
        )

        await state.clear()
    else:
        await msg.answer("Пожалуйста, отправьте контакт, используя кнопку.")
