from datetime import datetime

class Guest:
    def __init__(
            self,
            id: int = None,
            reg_number: str = None,
            full_name_uz: str = None,
            full_name_ru: str = None,
            table_number: int = None,
            persons_count: int = None,
            is_reg_number_generated: bool = None,
            phone_number: str = None,
            is_registered: bool = None,
            is_entered: bool = None,
            telegram_id: int = None,
            created_at: datetime = None):
        self.id = id
        self.reg_number = reg_number
        self.full_name_uz = full_name_uz
        self.full_name_ru = full_name_ru
        self.table_number = table_number
        self.persons_count = persons_count
        self.is_reg_number_generated = is_reg_number_generated
        self.is_registered = is_registered
        self.created_at = created_at
        self.phone_number = phone_number
        self.is_entered = is_entered
        self.telegram_id = telegram_id

class BotUser:
    def __init__(
            self,
            id: int,
            lang: str = "uz"):
        self.id = id
        self.lang = lang