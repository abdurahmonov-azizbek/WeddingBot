from aiogram import Router, F
from aiogram.types import *
from logger import logger
from services import botuser_service, guest_service
from models import BotUser, Guest
from locales import t
from aiogram.fsm.context import FSMContext
import keyboards
from config import ADMINS
import uuid
import os
import pandas as pd


router = Router()

@router.message(F.text == "/admin")
async def admin_welcome(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        return
    
    bot_user = await botuser_service.get_by_id(user_id)
    if not bot_user:
        await message.answer(f"🇺🇿 Iltimos, tilni tanlang\n🇷🇺Пожалуйста, выберите язык", reply_markup=keyboards.langs)
        return
    
    lang = bot_user.lang
    await state.update_data(lang=lang)
    await message.answer(t("admin_welcome", lang), reply_markup=keyboards.get_admin_menu(lang))

@router.message(F.text.in_(["📊 Statistika", "📊 Статистика"]))
async def admin_stats(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        return

    # Get user language
    lang = "uz"
    bot_user = await botuser_service.get_by_id(user_id)
    if bot_user:
        lang = bot_user.lang

    # Get all guests
    all_guests = await guest_service.get_all()
    total_guests = len(all_guests)

    # Count entered guests properly (async + real logic)
    entered_guests = sum(1 for g in all_guests if g.is_entered)
    registered_guests = sum(1 for g in all_guests if g.is_registered)

    # Format and send stats
    stats_text = t("admin_stats", lang).format(
        total=total_guests,
        entered=entered_guests,
        registered=registered_guests
    )

    await message.answer(stats_text)


@router.message(F.text.in_(["🖨 Печать Excel", "🖨 Excel print"]))
async def print(message: Message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        return
    
    loading = await message.answer("⏳")
    guests = await guest_service.get_all()
    data = []
    for g in guests:
        data.append({
            "ID": g.id,
            "Reg Number": g.reg_number,
            "Full Name (UZ)": g.full_name_uz,
            "Full Name (RU)": g.full_name_ru,
            "Table Number": g.table_number,
            "Persons Count": g.persons_count,
            "Phone": g.phone_number,
            "Telegram ID": g.telegram_id,
            "Registered": "Yes" if g.is_registered else "No",
            "Entered": "Yes" if g.is_entered else "No",
            "Reg Number Generated": "Yes" if g.is_reg_number_generated else "No",
            "Created At": g.created_at.strftime("%Y-%m-%d %H:%M") if g.created_at else "",
        })

    

    excels_folder = "excels"
    if not os.path.exists(excels_folder):
        os.makedirs(excels_folder)
    filename = os.path.join(excels_folder, f"guests_{uuid.uuid4()}.xlsx")


    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

    await loading.delete()
    await message.answer_document(FSInputFile(filename))