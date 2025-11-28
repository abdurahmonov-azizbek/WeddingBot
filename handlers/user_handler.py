from aiogram import Router, F
from logger import logger
from aiogram.types import *
from services import botuser_service, guest_service
from models import BotUser, Guest
from locales import t
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import keyboards
import functions as fn
import os
from config import HOSTESS

class RegStates(StatesGroup):
    lang = State()
    reg_number = State()
    phone_number = State()


router = Router()

@router.message(F.text == "/start")
async def welcome(message: Message, state: FSMContext):
    user_id = message.from_user.id
    bot_user = await botuser_service.get_by_id(user_id)
    if not bot_user:
        await state.set_state(RegStates.lang)
        await message.answer(f"🇺🇿 Iltimos, tilni tanlang\n🇷🇺Пожалуйста, выберите язык", reply_markup=keyboards.langs)
        return
    
    lang = bot_user.lang
    guest = await guest_service.get_by_telegram_id(user_id)
    if not guest:
        await message.answer(t("welcome", lang), reply_markup=keyboards.get_start_keyboard(lang))
        return
    
    await state.update_data(lang=lang)
    await message.answer(t("welcome", lang), reply_markup=keyboards.get_main_menu(lang))


    # await state.set_state(RegStates.reg_number)
    # await message.answer(t("enter_reg_number", lang))

@router.message(RegStates.lang)
async def set_lang(message: Message, state: FSMContext):
    text = message.text
    if text == "🇺🇿O'zbekcha":
        lang = "uz"
    elif text == "🇷🇺Русский":
        lang = "ru"
    else:
        await message.answer("Iltimos, quyidagi tugmalardan birini tanlang.\nПожалуйста, выберите одну из кнопок ниже.")
        return

    user_id = message.from_user.id
    bot_user = BotUser(id=user_id, lang=lang)
    await botuser_service.create(bot_user)

    await state.clear()
    await message.answer(t("lang_set", lang), reply_markup=keyboards.get_start_keyboard(lang))
    await message.answer(t("welcome", lang))

@router.message(F.text.in_(["🚀 Ro'yhatdan o'tish", "🚀 Зарегистрироваться"]))
async def register_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    bot_user = await botuser_service.get_by_id(user_id)
    if not bot_user:
        await state.clear()
        await message.answer(t("unexpected_error", "ru"))
        return
    
    lang = bot_user.lang

    guest = await guest_service.get_by_telegram_id(user_id)
    if guest:
        await message.answer(t("already_registered", lang), reply_markup=keyboards.get_main_menu(lang))
        return

    await state.update_data(lang=lang)
    await state.set_state(RegStates.reg_number)
    await message.answer(t("enter_reg_number", lang), reply_markup=keyboards.ReplyKeyboardRemove())

@router.message(RegStates.reg_number)
async def enter_reg_number(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    reg_number = message.text.strip()
    guest = await guest_service.get_by_reg_number(reg_number)
    if not guest: 
        #try to get by full name
        guest = await guest_service.get_by_name(reg_number)
    
    if not guest:
        await state.clear()
        await message.answer(t("reg_not_found", lang))
        return

    await state.update_data(reg_number=reg_number)
    await state.set_state(RegStates.phone_number)
    await message.answer(t("send_phone", lang), reply_markup=keyboards.get_contact_keyboard(t("phone_button", lang)))

@router.message(RegStates.phone_number)
async def save_info(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    reg_number = data.get("reg_number")

    if message.contact and message.contact.phone_number:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text.strip()

    guest = await guest_service.get_by_reg_number(reg_number)
    if not guest:
        guest = await guest_service.get_by_name(reg_number)

    if not guest:
        await state.clear()
        await message.answer(t("reg_not_found", lang))
        return

    guest.phone_number = phone_number
    guest.is_registered = True
    guest.telegram_id = message.from_user.id
    await guest_service.update(guest=guest)

    await state.clear()
    # await message.answer(t("invitation_ready", lang), reply_markup=keyboards.get_main_menu(lang))

    qr = fn.create_guest_qr(guest, lang)
    invitation_path = fn.create_invitation(qr, guest.full_name_uz if lang == "uz" else guest.full_name_ru, guest.table_number, guest.persons_count)
    await message.answer_photo(photo=FSInputFile(invitation_path), caption=t("invitation_ready", lang), reply_markup=keyboards.get_main_menu(lang))
    # os.remove(qr)

@router.message(F.text.in_(["🇺🇿 Til o'zgartirish", "🇷🇺 Изменить язык", "/lang"]))
async def change_language(message: Message):
    await message.answer("🇺🇿 Iltimos, tilni tanlang\n🇷🇺Пожалуйста, выберите язык", reply_markup=keyboards.lang_inline_keyboard)


class InvitationStates(StatesGroup):
    keyword = State()

@router.message(F.text.in_(["📩 Taklifnomani olish", "📩 Получить пригласительный"]))
async def get_invitation(message: Message, state: FSMContext):
    user_id = message.from_user.id
    bot_user = await botuser_service.get_by_id(user_id)
    if not bot_user:
        await state.clear()
        await message.answer("There is a error with your profile settings, please contact support.")
        return
    
    guest = await guest_service.get_by_telegram_id(user_id)
    if not guest:
        await message.answer(t("you_are_not_registered", bot_user.lang), reply_markup=keyboards.get_main_menu(bot_user.lang)) 
        return

    qr = fn.create_guest_qr(guest, bot_user.lang)
    invitation_path = fn.create_invitation(qr, guest.full_name_uz if bot_user.lang == "uz" else guest.full_name_ru, guest.table_number, guest.persons_count)
    await message.answer_photo(photo=FSInputFile(invitation_path), caption=t("invitation_ready", bot_user.lang), reply_markup=keyboards.get_main_menu(bot_user.lang))
    return

# @router.message(InvitationStates.keyword)
# async def send_invitation(message: Message, state: FSMContext):
#     data = await state.get_data()
#     lang = data.get("lang", "uz")

#     reg_number = message.text.strip()
#     guest = await guest_service.get_by_reg_number(reg_number)
#     if not guest:
#         #try to get by full name
#         guest = await guest_service.get_by_name(reg_number)

#     if not guest:
#         await state.clear()
#         await message.answer(t("reg_not_found", lang))
#         return
    
#     if not guest.is_registered:
#         await state.clear()
#         await message.answer(t("not_registered_yet", lang), reply_markup=keyboards.get_main_menu(lang))
#         return
    

#     qr_path = fn.create_guest_qr(guest, lang)
#     if not qr_path or not os.path.exists(qr_path):
#         await state.clear()
#         await message.answer(t("unexpected_error", lang), reply_markup=keyboards.get_main_menu(lang))
#         return
    
#     invitation_path = fn.create_invitation(qr_path, guest.full_name_uz if lang == "uz" else guest.full_name_ru, guest.table_number)
#     await message.answer_photo(photo=FSInputFile(invitation_path), caption=t("invitation_ready", lang), reply_markup=keyboards.get_main_menu(lang))
    