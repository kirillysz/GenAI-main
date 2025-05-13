# заменить в keyboards/inline ссылку на webapp

from aiogram import Bot, Dispatcher

from handlers import user_messages
from conifg import TOKEN

from asyncio import run

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(
        user_messages.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    run(main())