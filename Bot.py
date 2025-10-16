import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 Token va admin ID (o'zingnikini yoz)
TOKEN = "8231638131:AAEVZYNI9Iab_UCvS2KzFArQ9Fie08FZpuI"
ADMIN_ID = 1025705317

# Majburiy kanal linklari
CHANNEL_1 = "https://t.me/kanal1_link"
CHANNEL_2 = "https://t.me/kanal2_link"

# Foydalanuvchi ma’lumotlari
users = {}

# 🔹 Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users[user_id] = users.get(user_id, {"subscribed": False, "paid": False})

    text = (
        f"Salom, {update.effective_user.first_name}!\n\n"
        f"Botdan foydalanish uchun quyidagi kanallarga azo bo‘ling:\n"
        f"👉 {CHANNEL_1}\n"
        f"👉 {CHANNEL_2}\n\n"
        f"So‘ngra /check buyrug‘ini yuboring."
    )
    await update.message.reply_text(text)

# 🔹 Kanal a’zolikni tekshirish
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Bu joyda kanalga azo bo‘lganini tekshirish (Railway’da real ishlaydi)
    try:
        member1 = await context.bot.get_chat_member(chat_id="@kanal1_link", user_id=user_id)
        member2 = await context.bot.get_chat_member(chat_id="@kanal2_link", user_id=user_id)
        if member1.status not in ["member", "administrator", "creator"] or member2.status not in ["member", "administrator", "creator"]:
            await update.message.reply_text("Iltimos, ikkala kanalga ham azo bo‘ling va /check ni qayta yuboring.")
            return
    except:
        await update.message.reply_text("Kanalga azo bo‘lganingizni tekshirib bo‘lmadi. Linklar noto‘g‘ri bo‘lishi mumkin.")
        return

    users[user_id]["subscribed"] = True
    await update.message.reply_text("✅ Siz barcha kanallarga a’zo bo‘ldingiz!\nEndi /menu buyrug‘ini yuboring.")

# 🔹 Menyu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎥 Video yuklash", callback_data="video")],
        [InlineKeyboardButton("🎵 Musiqa topish", callback_data="music")],
        [InlineKeyboardButton("📊 Profil", callback_data="profile")],
        [InlineKeyboardButton("👑 Admin panel", callback_data="admin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Asosiy menyu:", reply_markup=reply_markup)

# 🔹 Callback tugmalar
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "video":
        await query.edit_message_text("🎥 YouTube havolasini yuboring:")
    elif query.data == "music":
        await query.edit_message_text("🎵 Musiqa izlash uchun YouTube havolasini yuboring:")
    elif query.data == "profile":
        user_id = query.from_user.id
        info = users.get(user_id, {"subscribed": False, "paid": False})
        await query.edit_message_text(f"👤 ID: {user_id}\n🔗 Obuna: {info['subscribed']}\n💰 To‘lov: {info['paid']}")
    elif query.data == "admin":
        if query.from_user.id == ADMIN_ID:
            await query.edit_message_text("👑 Admin panel:\n\n/sendall — xabar yuborish\n/stats — statistikani ko‘rish")
        else:
            await query.edit_message_text("Siz admin emassiz!")

# 🔹 Video yoki musiqa yuklash
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    user_id = update.message.from_user.id

    if not users.get(user_id, {}).get("subscribed"):
        await update.message.reply_text("Iltimos, avval kanallarga a’zo bo‘ling va /check yuboring.")
        return

    await update.message.reply_text("🔄 Yuklanmoqda... kuting...")

    ydl_opts = {"outtmpl": "video.%(ext)s"}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        await update.message.reply_video(video=open(filename, "rb"))
        os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {e}")

# 🔹 Admin buyruqlari
async def sendall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return await update.message.reply_text("Siz admin emassiz.")
    msg = update.message.text.replace("/sendall", "").strip()
    for user in users.keys():
        try:
            await context.bot.send_message(chat_id=user, text=msg)
        except:
            pass
    await update.message.reply_text("✅ Xabar yuborildi.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    total = len(users)
    await update.message.reply_text(f"👥 Foydalanuvchilar soni: {total}")

# 🔹 Botni ishga tushirish
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("sendall", sendall))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.add_handler(MessageHandler(filters.COMMAND, handle_link))
    app.run_polling()

if __name__ == "__main__":
    main()
