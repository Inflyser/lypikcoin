import asyncio

from aiogram import Router, Dispatcher, Bot, F
from aiogram.types import Message, CallbackQuery, WebAppInfo
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
   
def webapp_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Лупик-Coin ждет тебя!", web_app=WebAppInfo(
            url="https://4aaa-188-116-131-61.ngrok-free.app")
        )
    return builder.as_markup()

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.reply(
        "Лупа - Залупа, жми на кликер и лутай свой CASH!",
        reply_markup = webapp_builder()
    )
    
async def main():
    bot = Bot("7466156735:AAGrOcsjHH1Esjt_ztCWOu61FVcn4QJRCL0", parse_mod = ParseMode.HTML)
    
    dp = Dispatcher()
    dp.include_router(router)
    
    await bot.delete_webhook(True)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())