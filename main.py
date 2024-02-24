import asyncio
import re

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from loguru import logger

from kb import form_cancel_kb, cancel_button_kb
from states_group import GetInfo, not_in_state_filter
from generating import create_signatures

bot = Bot(token="6741119014:AAHbiM9bKqTRK36ijLMG5FR1albizZN0vPw", parse_mode=ParseMode.HTML)

dp = Dispatcher()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot successfully launched!")
    await dp.start_polling(bot)


# --- Основная панель -> Ввод имени ---
@dp.message(not_in_state_filter, Command("start", "generate"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(text="<b>Давайте знакомиться!</b>\n\nКак Вас зовут? Введите имя в чат:", reply_markup=form_cancel_kb())
    await state.set_state(GetInfo.firstname)


# --- Завершение заполнения формы по кнопке отмены ---
@dp.message(F.text == cancel_button_kb)
async def cancel_func(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(
            text="Нет формы, заполнение которой можно было бы прервать!",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            text="Заполнение формы прервано!",
            reply_markup=ReplyKeyboardRemove()
        )
    await state.clear()


# --- Ввод имени -> ввод фамилии ---
@dp.message(GetInfo.firstname)
async def step_firstname(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        return

    data = await state.get_data()
    message_text = re.sub(r'[^a-zA-Zа-яА-Я]', '', message.text[:10]).capitalize()
    if message_text != "":
        data['firstname'] = message_text
        await state.update_data(data)

        await message.answer(text=f"Супер, {message_text}, введите свою фамилию:")
        await state.set_state(GetInfo.lastname)
    else:
        await message.answer(text="Некорректно введено имя!")


# --- Ввод фамилии -> отправка подписи ---
@dp.message(GetInfo.lastname)
async def step_lastname(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        return

    data = await state.get_data()
    message_text = re.sub(r'[^a-zA-Zа-яА-Я]', '', message.text[:20]).capitalize()
    if message_text != "":
        data['lastname'] = message_text
        await state.update_data(data)

        firstname = data.get('firstname', 'Пусто')
        lastname = data.get('lastname', 'Пусто')

        font_number = create_signatures(
            firstname=firstname,
            lastname=lastname,
            user_id=message.from_user.id
        )
        await message.answer_photo(
            photo=FSInputFile(f"assets/users_signature/{message.from_user.id}_{font_number}.png"),
            caption=f"Рад знакомству, {firstname} {lastname}!",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
    else:
        await message.answer(text="Некорректно введена фамилия!")


if __name__ == "__main__":
    asyncio.run(main())
