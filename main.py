from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio
import os
from modules import music, economy
from config import BOT_TOKEN, ADMIN_ID, CARD_NUMBER

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ————— Start
@dp.message(Command("start"))
async def start(msg: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.button(text="🎥 Video yuklash")
    kb.button(text="🎵 Musiqa topish")
    kb.button(text="💳 To‘lov qilish")
    kb.button(text="👤 Profil")
    await msg.answer("Assalomu alaykum!\nTanlang 👇", reply_markup=kb.as_markup(resize_keyboard=True))

# ————— Musiqa qidirish
@dp.message(F.text == "🎵 Musiqa topish")
async def music_menu(msg: types.Message):
    await msg.answer("🎧 Musiqa nomini yozing yoki ovozli xabar yuboring:")
    
@dp.message(F.voice)
async def handle_voice(msg: types.Message):
    await music.handle_voice_message(msg)

@dp.callback_query(F.data.startswith("dl_audio|"))
async def dl_audio(cq: types.CallbackQuery):
    _, url = cq.data.split("|", 1)
    await music.cb_download_audio(cq, url)

@dp.message(F.text & ~F.command)
async def handle_text(msg: types.Message):
    text = msg.text.strip()
    await music.search_and_offer(msg, text)

# ————— To‘lov qilish
@dp.message(F.text == "💳 To‘lov qilish")
async def pay(msg: types.Message):
    await msg.answer(f"💰 To‘lov uchun karta:\n{CARD_NUMBER}\n\nTo‘lovni amalga oshirgach, adminga yozing: @{ADMIN_ID}")

# ————— Profil
@dp.message(F.text == "👤 Profil")
async def profile(msg: types.Message):
    await msg.answer("Sizning profilingiz hozircha soddalashtirilgan versiyada.")

# ————— Run bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
