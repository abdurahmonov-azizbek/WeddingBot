from bot_instance import bot, dp
import asyncio
from logger import logger
from handlers.user_handler import router as user_router
from handlers.base_handler import router as base_router
from handlers.hostes_handler import router as hostes_router
from handlers.admin_handler import router as admin_router

dp.include_router(base_router)
dp.include_router(user_router)
dp.include_router(hostes_router)
dp.include_router(admin_router)

async def main():
    logger.info("Starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())