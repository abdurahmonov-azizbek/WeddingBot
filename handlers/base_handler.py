from aiogram import Router, F
from aiogram.types import *
from logger import logger
from services import botuser_service, guest_service
from models import BotUser, Guest
from locales import t
from aiogram.fsm.context import FSMContext
import keyboards
from config import HOSTESS, ADMINS

router = Router()

@router.message(F.text.in_(["🔙 Отмена", "🔙 Bekor qilish"]))
async def cancel_registration(message: Message, state: FSMContext):
    if state:
        await state.clear()

    await message.answer("✅")


@router.callback_query(F.data.startswith("set_lang:"))
async def callback_set_lang(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    lang = data.split(":")[1]
    user_id = callback.from_user.id
    bot_user = await botuser_service.get_by_id(user_id)
    if bot_user:
        bot_user.lang = lang
        await botuser_service.update_lang(bot_user.id, lang)
    else:
        bot_user = BotUser(id=user_id, lang=lang)
        await botuser_service.create(bot_user)

    await callback.answer()
    await callback.message.delete()
    if user_id in HOSTESS:
        await callback.message.answer(t("lang_set", lang), reply_markup=keyboards.get_hostes_menu(lang))
    elif user_id in ADMINS: 
        await callback.message.answer(t("lang_changed", lang), reply_markup=keyboards.get_admin_menu(lang))
    else:
        await callback.message.answer(t("lang_set", lang), reply_markup=keyboards.get_main_menu(lang))
