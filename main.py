from aiogram import Bot, Dispatcher
import asyncio

from app.handlers import rt
from db.executors import init

TOKEN = ""

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await init()
    dp.include_router(rt)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())