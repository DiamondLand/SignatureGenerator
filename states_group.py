from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from kb import cancel_button_kb


# --- StatesGroup для регистрации аккаунта ---
class GetInfo(StatesGroup):
    firstname = State()
    lastname = State()


# --- Блокирующий фильтр для команд во время стадий ---
not_in_state_filter = ~StateFilter(
    GetInfo.firstname,
    GetInfo.lastname
)
