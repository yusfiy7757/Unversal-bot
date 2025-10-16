import os
import tempfile
from yt_dlp import YoutubeDL
from aiogram import types
from utils.voice import voice_to_text

YTDL_OPTS = {"quiet": True, "noplaylist": True}

async def search_and_offer(message: types.Message, query: str):
    await message.reply("🔎 Qidirilyapti...")
    with YoutubeDL(YTDL_OPTS) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
    if not info:
        return await message.reply("❌ Natija topilmadi.")
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton("▶ Tinglash", url=info.get("webpage_url"))],
        [types.InlineKeyboardButton("📥 Yuklab olish (mp3)", callback_data=f"dl_audio|{info.get('webpage_url')}")]
    ])
    await message.reply(f"✅ {info.get('title')}", reply_markup=kb)

async def handle_voice_message(message: types.Message):
    await message.reply("🎧 Audio o'qilmoqda...")
    file = await message.voice.download()
    path = file.name
    text = voice_to_text(path)
    try:
        os.remove(path)
    except:
        pass
    if not text:
        return await message.reply("⚠️ Audio orqali nom aniqlanmadi. Qo‘lda yozing.")
    return await search_and_offer(message, text)

async def cb_download_audio(callback_query: types.CallbackQuery, url: str):
    await callback_query.message.edit_text("⏳ Yuklanmoqda...")
    with tempfile.TemporaryDirectory() as td:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{td}/%(title)s.%(ext)s",
            "quiet": True
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        await callback_query.message.answer_audio(open(file_path, "rb"), caption=info.get("title"))
