import asyncio

from aiogram import Router, Dispatcher, Bot, F
from aiogram.types import Message, CallbackQuery, WebAppInfo
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models import asyns_main
import request0 as rq

def webapp_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Лупик-Coin ждет тебя!", web_app=WebAppInfo(
        url="https://a7a0-188-116-131-61.ngrok-free.app"),
        
        )  
    
    return builder.as_markup()

router = Router()
# Лупа - Залупа, жми на кликер и лутай свой кеш!
message_pablic = "Жми и лутай лупик-койны."
C = "Жми Жми"

@router.message(CommandStart())
async def start(message: Message):
    await rq.set_user(message.from_user.id)
    await rq.update_name(message.from_user.id, message.from_user.first_name)
    
    await message.answer(f"Пользователь: {message.from_user.first_name}")
    await message.answer("Ваш ID: ")
    await message.answer(f"```\n{message.from_user.id}\n```", parse_mode="MarkdownV2")
    await message.reply(
        message_pablic,
        reply_markup = webapp_builder()
    )
    
    
async def main():
    await asyns_main()
    bot = Bot("7466156735:AAGrOcsjHH1Esjt_ztCWOu61FVcn4QJRCL0", parse_mod = ParseMode.HTML)
    
    dp = Dispatcher()
    dp.include_router(router)
    
    await bot.delete_webhook(True)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:    
        print("Бот выключен.")
