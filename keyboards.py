from aiogram.types import *


lang_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [ 
        InlineKeyboardButton(text="Русский 🇷🇺", callback_data="set_lang:ru"),
        InlineKeyboardButton(text="O'zbekcha 🇺🇿", callback_data="set_lang:uz"),
    ]
])

hostes_back = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="🔙"),]
    ]
)

lang_inline_for_hostes = InlineKeyboardMarkup(inline_keyboard=[
    [ 
        InlineKeyboardButton(text="Русский 🇷🇺", callback_data="set_lang_hostes:ru"),
        InlineKeyboardButton(text="O'zbekcha 🇺🇿", callback_data="set_lang_hostes:uz"),
    ]
])

langs = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="🇺🇿O'zbekcha"), KeyboardButton(text="🇷🇺Русский")]
    ]
)

def get_start_keyboard(lang) -> ReplyKeyboardMarkup:
    if lang == "ru":
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text="🚀 Зарегистрироваться")]
            ]
        )
        
    else:
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text="🚀 Ro'yhatdan o'tish")]
            ]
        )

def get_cancel_keyboard(lang):
    if lang == "ru":
        cancel_keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text="🔙 Отмена")]
            ]
        )
    else:
        cancel_keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text="🔙 Bekor qilish")]
            ]
        )
    return cancel_keyboard

def get_hostes_menu(lang: str) -> ReplyKeyboardMarkup:
    if lang == "ru":
        hostes_menu = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text="📋 Отметить как вошедшего")],
                [KeyboardButton(text="🇷🇺 Изменить язык")],
            ]
        )
    else:
        hostes_menu = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text="📋 Kirdi deb belgilash")],
                [KeyboardButton(text="🇺🇿 Til o'zgartirish")],
            ]
        )
    return hostes_menu


def get_main_menu(lang: str) -> ReplyKeyboardMarkup:
    if lang == "ru":
        main_menu = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text="📩 Получить пригласительный")],
                [KeyboardButton(text="🇷🇺 Изменить язык")],
            ]
        )
    else:
        main_menu = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text="📩 Taklifnomani olish")],
                [KeyboardButton(text="🇺🇿 Til o'zgartirish")],
            ]
        )
    return main_menu


def get_contact_keyboard(button_text) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text=button_text, request_contact=True)]
        ]
    )
    return keyboard

def get_admin_menu(lang: str) -> ReplyKeyboardMarkup:
    if lang == "ru":
        admin_menu = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text="📊 Статистика")],
                [KeyboardButton(text="🖨 Печать Excel")],
                [KeyboardButton(text="🇷🇺 Изменить язык")],
            ]
        )
    else:
        admin_menu = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text="📊 Statistika")],
                [KeyboardButton(text="🖨 Excel print")],
                [KeyboardButton(text="🇺🇿 Til o'zgartirish")],
            ]
        )
    return admin_menu