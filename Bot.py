import os
import json
import yt_dlp
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# 🧾 TOKEN va ADMIN_ID
TOKEN = "8231638131:AAEVZYNI9Iab_UCvS2KzFArQ9Fie08FZpuI"
ADMIN_ID = 1025705317

# 💳 To‘lov ma’lumotlari
CARD_NUMBER = "9860160130908306 Yusufjanov Bilolxon"

# 📁 Fayllar
USERS_FILE = "users.json"
CHANNELS_FILE = "channels.json"

# 🔰 Ma’lumotlarni yuklash
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

if os.path.exists(CHANNELS_FILE):
    with open(CHANNELS_FILE, "r") as f:
        channels = json.load(f)
else:
    channels = ["https://t.me/example1", "https://t.me/example2"]

# 🔒 Ma’lumotlarni saqlash
def save_data():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)
    with open(CHANNELS_FILE, "w") as f:
        json.dump(channels, f)

# 🎬 /start buyrug‘i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)

    if user_id not in users:
        users[user_id] = {"paid": False, "subscribed": False}
        save_data()

    if not users[user_id]["subscribed"]:
        text = "🔔 Botdan foydalanish uchun quyidagi 2 ta kanalga obuna bo‘ling:\n\n"
        for ch in channels:
            text += f"👉 {ch}\n"
        text += "\nObuna bo‘lgach, /check buyrug‘ini bosing ✅"
        await update.message.reply_text(text)
    else:
        await show_menu(update)

# ✅ Obunani tekshirish
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    users[user_id]["subscribed"] = True
    save_data()
    await update.message.reply_text("✅ Obuna tasdiqlandi!")
    await show_menu(update)

# 📋 Menyu
async def show_menu(update: Update):
    keyboard = [
        [KeyboardButton("🎥 Video yuklash"), KeyboardButton("🎵 Musiqa qidirish")],
        [KeyboardButton("💳 To‘lov qilish"), KeyboardButton("👤 Profil")],
        [KeyboardButton("🛠 Admin panel")]
    ]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Tanlang 👇", reply_markup=markup)

# 💳 To‘lov qilish
async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    users[user_id]["paid"] = True
    save_data()
    await update.message.reply_text(
        f"✅ To‘lov qabul qilindi!\nEndi cheklovlarsiz foydalanishingiz mumkin.\n\n💳 Karta: {CARD_NUMBER}"
    )
    await context.bot.send_message(ADMIN_ID, f"💰 {user_id} foydalanuvchi to‘lov amalga oshirdi.")

# 👤 Profil
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    data = users.get(user_id, {})
    text = f"""
👤 Profil ma’lumotlari:
🆔 ID: {user_id}
📢 Obuna: {data.get('subscribed', False)}
💳 To‘lov: {data.get('paid', False)}
"""
    await update.message.reply_text(text)

# 🎥 Video yuklash
async def video_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎥 Video havolasini yuboring:")
    context.user_data["mode"] = "video"

# 🎵 Musiqa qidirish
async def music_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 Qaysi qo‘shiqni qidiray?")
    context.user_data["mode"] = "music"

# 🧠 Foydalanuvchi javobi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    text = update.message.text
    mode = context.user_data.get("mode")

    if mode == "video":
        await download_video(update, text)
    elif mode == "music":
        await search_music(update, text)
    else:
        await update.message.reply_text("Menyudan birini tanlang 👇")

# 🎬 YouTube video yuklash
async def download_video(update, url):
    await update.message.reply_text("⏳ Yuklanmoqda...")

    ydl_opts = {
        "format": "best[ext=mp4]",
        "outtmpl": "video.mp4"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await update.message.reply_video(open("video.mp4", "rb"))
        os.remove("video.mp4")

    except Exception as e:
        await update.message.reply_text(f"❌ Xato: {e}")

# 🎵 Musiqa yuklash (YouTube orqali)
async def search_music(update, query):
    await update.message.reply_text("🔎 Qidirilmoqda...")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "audio.mp3",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            await update.message.reply_audio(open("audio.mp3", "rb"), title=info["entries"][0]["title"])
            os.remove("audio.mp3")
    except Exception as e:
        await update.message.reply_text(f"❌ Xato: {e}")

# 🛠 Admin panel
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    if user_id != str(ADMIN_ID):
        await update.message.reply_text("⛔ Siz admin emassiz.")
        return

    keyboard = [
        [InlineKeyboardButton("📢 Kanallarni ko‘rish", callback_data="view_channels")],
        [InlineKeyboardButton("➕ Kanal qo‘shish", callback_data="add_channel")],
        [InlineKeyboardButton("🗑 Kanal o‘chirish", callback_data="delete_channel")],
        [InlineKeyboardButton("📊 Statistika", callback_data="stats")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🛠 Admin paneli:", reply_markup=markup)

# ⚙️ Admin tugmalari
async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "view_channels":
        text = "📢 Majburiy kanallar:\n" + "\n".join(channels)
        await query.message.reply_text(text)

    elif query.data == "add_channel":
        await query.message.reply_text("➕ Yangi kanal linkini yuboring:")
        context.user_data["admin_mode"] = "add_channel"

    elif query.data == "delete_channel":
        await query.message.reply_text("🗑 O‘chiriladigan kanal linkini yuboring:")
        context.user_data["admin_mode"] = "delete_channel"

    elif query.data == "stats":
        await query.message.reply_text(f"📊 Foydalanuvchilar soni: {len(users)} ta")

# 🧩 Admin kanal o‘zgartirish
async def admin_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get("admin_mode")

    if mode == "add_channel":
        channels.append(update.message.text)
        save_data()
        await update.message.reply_text("✅ Kanal qo‘shildi!")
        context.user_data["admin_mode"] = None

    elif mode == "delete_channel":
        if update.message.text in channels:
            channels.remove(update.message.text)
            save_data()
            await update.message.reply_text("🗑 Kanal o‘chirildi!")
        else:
            await update.message.reply_text("❌ Bunday kanal topilmadi.")
        context.user_data["admin_mode"] = None

# 🧠 Asosiy bot
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_subscription))
    app.add_handler(CommandHandler("pay", pay))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(MessageHandler(filters.Regex("🎥 Video yuklash"), video_download))
    app.add_handler(MessageHandler(filters.Regex("🎵 Musiqa qidirish"), music_search))
    app.add_handler(MessageHandler(filters.Regex("💳 To‘lov qilish"), pay))
    app.add_handler(MessageHandler(filters.Regex("👤 Profil"), profile))
    app.add_handler(MessageHandler(filters.Regex("🛠 Admin panel"), admin_panel))
    app.add_handler(CallbackQueryHandler(admin_callback))
    app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN_ID), admin_text_handler))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
