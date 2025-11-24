import database
from models import Guest
from logger import logger

TABLE_NAME = "guest"


async def get_by_name(full_name: str):
    conn = await database.get_connection()
    query = f"SELECT * FROM {TABLE_NAME} WHERE full_name_uz = $1 OR full_name_ru = $1"

    try:
        row = await conn.fetchrow(query, full_name)
        if not row:
            logger.info(f"Guest with name {full_name} not found.")
            return None
        guest = Guest(**row)
        return guest
    except Exception as e:
        logger.error(f"Error fetching guest by name {full_name}: {e}")
        return None
    finally:
        await conn.close()

async def get_by_reg_number(reg_number: str):
    conn = await database.get_connection()
    query = f"SELECT * FROM {TABLE_NAME} WHERE reg_number = $1"

    try:
        row = await conn.fetchrow(query, reg_number)
        if not row:
            logger.info(f"Guest with reg number {reg_number} not found.")
            return None
        guest = Guest(**row)
        return guest
    except Exception as e:
        logger.error(f"Error fetching guest by reg number {reg_number}: {e}")
        return None
    finally:
        await conn.close()

async def get_by_telegram_id(telegram_id: int):
    conn = await database.get_connection()
    query = f"SELECT * FROM {TABLE_NAME} WHERE telegram_id = $1"

    try:
        row = await conn.fetchrow(query, telegram_id)
        if not row:
            logger.info(f"Guest with tg id {telegram_id} not found.")
            return None
        guest = Guest(**row)
        return guest
    except Exception as e:
        logger.error(f"Error fetching guest by reg number {telegram_id}: {e}")
        return None
    finally:
        await conn.close()

async def get_all():
    conn = await database.get_connection()
    query = f"SELECT * FROM {TABLE_NAME}"

    try:
        rows = await conn.fetch(query)
        guests = [Guest(**row) for row in rows]
        return guests
    except Exception as e:
        logger.error(f"Error fetching all guests: {e}")
        return []
    finally:
        await conn.close()

async def get_by_id(id: int):
    conn = await database.get_connection()
    query = f"SELECT * FROM {TABLE_NAME} WHERE id = $1"
    
    try:
        row = await conn.fetchrow(query, id)
        if not row:
            logger.info(f"Guest with id {id} not found.")
            return None
        guest = Guest(**row)
        return guest
    except Exception as e:
        logger.error(f"Error fetching guest by id {id}: {e}")
        return None
    finally:
        await conn.close()

async def create(guest: Guest):
    conn = await database.get_connection()
    query = f"""
    INSERT INTO {TABLE_NAME} (reg_number, full_name_uz, full_name_ru, table_number, persons_count, is_reg_number_generated, is_registered, created_at, phone_number, is_entered, telegram_id)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
    RETURNING id
    """
    
    try:
        guest_id = await conn.fetchval(
            query,
            guest.reg_number,
            guest.full_name_uz,
            guest.full_name_ru,
            guest.table_number,
            guest.persons_count,
            guest.is_reg_number_generated,
            guest.is_registered,
            guest.created_at,
            guest.phone_number,
            guest.is_entered,
            guest.telegram_id
        )
        guest.id = guest_id
        return guest
    except Exception as e:
        logger.error(f"Error creating guest: {e}")
        return None
    finally:
        await conn.close()


async def update(guest: Guest):
    conn = await database.get_connection()
    query = f"""
    UPDATE {TABLE_NAME}
    SET reg_number = $1,
        full_name_uz = $2,
        full_name_ru = $3,
        table_number = $4,
        persons_count = $5,
        is_reg_number_generated = $6,
        is_registered = $7,
        phone_number = $8,
        is_entered = $9,
        telegram_id = $10
    WHERE id = $11
    """
    
    try:
        await conn.execute(
            query,
            guest.reg_number,
            guest.full_name_uz,
            guest.full_name_ru,
            guest.table_number,
            guest.persons_count,
            guest.is_reg_number_generated,
            guest.is_registered,
            guest.phone_number,
            guest.is_entered,
            guest.telegram_id,
            guest.id
        )
        return True
    except Exception as e:
        logger.error(f"Error updating guest with id {guest.id}: {e}")
        return False
    finally:
        await conn.close()

async def delete_by_id(id: int):
    conn = await database.get_connection()
    query = f"DELETE FROM {TABLE_NAME} WHERE id = $1"
    
    try:
        await conn.execute(query, id)
        return True
    except Exception as e:
        logger.error(f"Error deleting guest with id {id}: {e}")
        return False
    finally:
        await conn.close()