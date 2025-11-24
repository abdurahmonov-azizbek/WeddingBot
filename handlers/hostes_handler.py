from aiogram import Router, F
from aiogram.types import *
from logger import logger
from services import botuser_service, guest_service
from models import BotUser, Guest
from locales import t
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import keyboards
import functions as fn
import os
from config import HOSTESS

router = Router()

@router.message(F.text == "/host")
async def hostess_welcome(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in HOSTESS:
        return
    
    bot_user = await botuser_service.get_by_id(user_id)
    if not bot_user:
        await message.answer(f"🇺🇿 Iltimos, tilni tanlang\n🇷🇺Пожалуйста, выберите язык", reply_markup=keyboards.lang_inline_for_hostes)
        return
    
    lang = bot_user.lang
    await state.update_data(lang=lang)
    await message.answer(t("hostess_welcome", lang), reply_markup=keyboards.get_hostes_menu(lang))

@router.callback_query(F.data.startswith("set_lang_hostes:"))
async def set_hostess_lang(callback_query: CallbackQuery, state: FSMContext):
    lang = callback_query.data.split(":")[1]
    user_id = callback_query.from_user.id

    if user_id not in HOSTESS:
        return

    bot_user = await botuser_service.get_by_id(user_id)
    if not bot_user:
        bot_user = BotUser(id=user_id, lang=lang)
        await botuser_service.create(bot_user)
    else:
        bot_user.lang = lang
        await botuser_service.update_lang(bot_user.id, lang)

    await callback_query.message.answer(t("lang_set", lang), reply_markup=keyboards.get_hostes_menu(lang))
    await callback_query.answer()

class HostessStates(StatesGroup):
    keyword = State()

@router.message(F.text.in_(["📋 Kirdi deb belgilash", "📋 Отметить как вошедшего"]))
async def mark_guest_entered(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in HOSTESS:
        return

    bot_user = await botuser_service.get_by_id(user_id)
    lang = bot_user.lang if bot_user else "uz"
    data = await state.get_data()
    await state.update_data(lang=lang)

    await state.set_state(HostessStates.keyword)
    await message.answer(t("enter_reg_or_name", lang), reply_markup=keyboards.hostes_back)

@router.message(HostessStates.keyword)
async def process_mark_entered(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in HOSTESS:
        return

    data = await state.get_data()
    lang = data.get("lang", "uz")

    reg_or_name = message.text.strip()
    if reg_or_name == "🔙":
        await state.clear()
        await message.answer("✅", reply_markup=keyboards.get_hostes_menu(lang))
        return
    
    guest = await guest_service.get_by_reg_number(reg_or_name)
    if not guest:
        guest = await guest_service.get_by_name(reg_or_name)

    if not guest:
        await state.clear()
        await message.answer(t("reg_not_found", lang), reply_markup=keyboards.get_hostes_menu(lang))
        return

    if guest.is_entered:
        await state.clear()
        await message.answer(t("guest_already_entered", lang), reply_markup=keyboards.get_hostes_menu(lang))
        return

    guest.is_entered = True
    await guest_service.update(guest)
    await state.clear()
    await message.answer("✅", reply_markup=keyboards.get_hostes_menu(lang))