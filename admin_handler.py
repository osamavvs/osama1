import telebot
import os

# نستخدم نفس التوكن الموجود في ملفك الرئيسي
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_ID = 8074717568  # الأيدي الخاص بك

@bot.message_handler(commands=['admin'])
def admin_menu(message):
    if message.from_user.id == ADMIN_ID:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text="📊 عدد المستخدمين", callback_data="stats"))
        markup.add(telebot.types.InlineKeyboardButton(text="📢 إذاعة", callback_data="broadcast"))
        bot.reply_to(message, "👑 أهلاً بك يا أدمن، هذه لوحة تحكم إضافية:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "stats":
        bot.answer_callback_query(call.id, "البوت يعمل بشكل طبيعي")
    elif call.data == "broadcast":
        bot.edit_message_text("أرسل رسالة الإذاعة الآن:", call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(call.message, do_broadcast)

def do_broadcast(message):
    bot.reply_to(message, "✅ جاري الإرسال...")
    # ملاحظة: هذا الملف لا يعرف المستخدمين إلا إذا سجلتهم في قاعدة بيانات
    # هذا الكود بسيط للتحكم دون لمس الكود الرئيسي
