import database
from models import BotUser
from logger import logger

TABLE_NAME = "bot_user"

async def get_by_id(id: int):
    conn = await database.get_connection()
    query = f"SELECT * FROM {TABLE_NAME} WHERE id = $1"
    
    try:
        row = await conn.fetchrow(query, id)
        if not row:
            logger.info(f"BotUser with id {id} not found.")
            return None
        bot_user = BotUser(**row)
        return bot_user
    except Exception as e:
        logger.error(f"Error fetching BotUser by id {id}: {e}")
        return None
    finally:
        await conn.close()

async def create(bot_user: BotUser):
    conn = await database.get_connection()
    query = f"""
    INSERT INTO {TABLE_NAME} (id, lang)
    VALUES ($1, $2)
    RETURNING id
    """
    
    try:
        bot_user_id = await conn.fetchval(
            query,
            bot_user.id,
            bot_user.lang
        )
        return bot_user_id
    except Exception as e:
        logger.error(f"Error creating BotUser with id {bot_user.id}: {e}")
        return None
    finally:
        await conn.close()

async def update_lang(id: int, lang: str):
    conn = await database.get_connection()
    query = f"""
    UPDATE {TABLE_NAME}
    SET lang = $1
    WHERE id = $2
    """
    
    try:
        await conn.execute(query, lang, id)
        return True
    except Exception as e:
        logger.error(f"Error updating lang for BotUser with id {id}: {e}")
        return False
    finally:
        await conn.close()