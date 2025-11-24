from enum import StrEnum
from typing import Literal

class Lang(StrEnum):
    RU = "ru"
    UZ = "uz"

# Все тексты в одном месте — легко править клиенту
TEXTS = {
    # Приветствие
    "welcome": {
        Lang.RU: "🎉 Добро пожаловать!\n\nЮбилейный Банкет Директоров Oriflame 2025\n\nНажмите кнопку, чтобы получить ваш электронный пригласительный",
        Lang.UZ: "🎉 Xush kelibsiz!\n\nOriflame Direktorlar Banketi 2025\n\nElektron taklifnomangizni olish uchun tugmani bosing"
    },
    "start_button": {
        Lang.RU: "🔥 Начать",
        Lang.UZ: "🔥 Boshlash"
    },
    "enter_reg_number": {
        Lang.RU: "Введите ваш регистрационный номер или имя и фамилию:",
        Lang.UZ: "Ro'yhatdan o'tish raqamingizni yoki ism familiyangizni kiriting:"
    },
    "reg_not_found": {
        Lang.RU: "❌ Регистрационный номер не найден.\nПроверьте правильность ввода или обратитесь к вашему спонсору.",
        Lang.UZ: "❌ Ro'yxat raqami topilmadi.\nIltimos, raqamni tekshiring yoki homiyingizga murojaat qiling."
    },
    "send_phone": {
        Lang.RU: "Отправьте ваш номер телефона, нажав кнопку ниже 👇",
        Lang.UZ: "Quyidagi tugmani bosib telefon raqamingizni yuboring 👇"
    },
    "phone_button": {
        Lang.RU: "📱 Отправить телефон",
        Lang.UZ: "📱 Telefonni yuborish"
    },
    "invitation_ready": {
        Lang.RU: "Ваш пригласительный готов!\n\nСохраните изображение и предъявите его на входе вместе с паспортом.",
        Lang.UZ: "Sizning taklifnomangiz tayyor!\n\nRasmni saqlang va kirishda pasport bilan birga ko'rsating."
    },
    "get_again_button": {
        Lang.RU: "🔄 Получить пригласительный снова",
        Lang.UZ: "🔄 Taklifnomani qayta olish"
    },
    "rules_caption": {
        Lang.RU: "⚠️ ВАЖНО!\n\nПригласительный действателен только с паспортом или ID-картой\n"
                  "Указано максимальное количество персон\n"
                  "Все дополнительные гости должны присутствовать одновременно\n"
                  "После регистрации дополнительные браслеты не выдаются\n\nС уважением, Oriflame ❤️",
        Lang.UZ: "⚠️ MUHIM!\n\nTaklifnoma faqat pasport yoki ID-karta bilan amal qiladi\n"
                  "Maksimal odamlar soni ko'rsatilgan\n"
                  "Qo‘shimcha mehmonlar bir vaqtda kelishi shart\n"
                  "Ro‘yxatdan o‘tgandan keyin qo‘shimcha bilaguzuk berilmaydi\n\nHurmat bilan, Oriflame ❤️"
    },

    # Хостесс часть
    "hostess_scan": {
        Lang.RU: "Сканировать QR-код гостя",
        Lang.UZ: "Mehmon QR-kodini skaner qilish"
    },
    "hostess_enter_manually": {
        Lang.RU: "Ввести номер вручную",
        Lang.UZ: "Raqamni qo‘lda kiritish"
    },
    "guest_info": {
        Lang.RU: "👤 ФИО: {name}\n👥 Количество персон: {persons}\n🪑 Стол: {table}\n\n",
        Lang.UZ: "👤 F.I.O: {name}\n👥 Odamlar soni: {persons}\n🪑 Stol: {table}\n\n"
    },
    "already_registered": {
        Lang.RU: "✅ Гость уже зарегистрирован\n⏰ Время: {time}",
        Lang.UZ: "✅ Mehmon allaqachon ro‘yxatdan o‘tgan\n⏰ Vaqt: {time}"
    },
    "register_button": {
        Lang.RU: "✅ Зарегистрировать прибытие",
        Lang.UZ: "✅ Kelishni ro‘yxatga olish"
    },
    "registered_success": {
        Lang.RU: "Гость успешно зарегистрирован!",
        Lang.UZ: "Mehmon muvaffaqiyatli ro‘yxatdan o‘tdi!"
    },
    "lang_changed": {
        Lang.RU: "Язык изменен на русский 🇷🇺",
        Lang.UZ: "Til o'zbekchaga o'zgartirildi 🇺🇿"
    },
    "lang_set": {
        Lang.RU: "Язык установлен",
        Lang.UZ: "Til o'rnatildi"
    },
    "not_registered_yet": {
        Lang.RU: "❌ Гость еще не зарегистрирован.",
        Lang.UZ: "❌ Mehmon hali ro‘yxatdan o‘tmagan."
    },
    "unexpected_error": {
        Lang.RU: "❌ Произошла непредвиденная ошибка. Пожалуйста, попробуйте еще раз.",
        Lang.UZ: "❌ Kutilmagan xatolik yuz berdi. Iltimos, qayta urinib ko‘ring."
    },
    "hostess_welcome":
    {
        Lang.RU: "👋 Добро пожаловать, Хостесс!\n\nИспользуйте меню ниже для управления гостями.",
        Lang.UZ: "👋 Xush kelibsiz, Xostess!\n\nQuyidagi menyudan mehmonlarni boshqarish uchun foydalaning."
    },
    "already_registered":{
        Lang.RU: "❌ Вы уже зарегистрированы.\nИспользуйте меню ниже.",
        Lang.UZ: "❌ Siz allaqachon ro'yxatdan o'tgansiz.\nQuyidagi menyudan foydalaning."
    },
    "enter_reg_or_name": {
        Lang.RU: "Введите регистрационный номер или полное имя гостя:",
        Lang.UZ: "Mehmonning ro'yxat raqamini yoki to'liq ismini kiriting:"
    },
    "guest_already_entered": {
        Lang.RU: "❌ Гость уже отмечен как вошедший.",
        Lang.UZ: "❌ Mehmon allaqachon kirdi deb belgilangan."
    },
    "you_are_not_registered": {
        Lang.UZ: "❌ Siz mehmon sifatida ro'yxatdan o'tmagansiz.",
        Lang.RU: "❌ Вы не зарегистрированы как гость."
    },
    "admin_welcome": {
        Lang.RU: "👋 Добро пожаловать, Администратор!\n\nИспользуйте меню ниже для управления ботом.",
        Lang.UZ: "👋 Xush kelibsiz, Administrator!\n\nQuyidagi menyudan botni boshqarish uchun foydalaning."
    },
    "admin_stats": {
        Lang.RU: "📊 Статистика по регистрации гостей:\n\nВсего гостей: {total}\nЗарегистрировано: {registered}\nВошло на банкет: {entered}",
        Lang.UZ: "📊 Mehmonlar ro‘yxatga olish bo‘yicha statistika:\n\nJami mehmonlar: {total}\nRo‘yxatdan o‘tganlar: {registered}\nBanketga kirganlar: {entered}"
    }
}

def t(key: str, lang: Lang) -> str:
    return TEXTS[key].get(lang, TEXTS[key][Lang.RU])