import telebot
import requests
import logging
import sys
import os
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import check  # استدعاء ملف الاشتراك

# برمجة @U_K44
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    welcome_text = "مرحبا بك في بوت رشق تفاعلات ومشاهدات بوست تليجرام مجانا 🚀\n\n• أرسل لي رابط المنشور لإضافة تفاعلات."
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="قناة البوت 📢", url="https://t.me/BBABB9"))
    markup.add(InlineKeyboardButton(text="المطور 👨‍💻", url="https://t.me/U_K44"))
    bot.reply_to(message, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    # التحقق عبر الملف المنفصل
    if not check.is_user_subscribed(bot, message.from_user.id):
        bot.reply_to(message, "❌ عذراً، يجب عليك الاشتراك في القناة أولاً:", reply_markup=check.get_sub_markup())
        return

    try:
        if not message.text.startswith(('http://', 'https://')):
            bot.reply_to(message, "❌ الرجاء إرسال رابط صحيح.")
            return

        link = message.text.strip()
        waiting_msg = bot.reply_to(message, "⏳ جاري معالجة طلبك...")
        
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'}
        json_data = {'link': link, 'quantity': '50', 'provider_service_id': '10949', 'username': 'guest'}

        response = requests.post('https://test.socialfruit.co/api/gateway', headers=headers, json=json_data, timeout=30)
        
        if "success" in response.text.lower():
            bot.edit_message_text("✅ تم بنجاح إضافة التفاعلات", chat_id=message.chat.id, message_id=waiting_msg.message_id)
        else:
            bot.edit_message_text("❌ فشلت العملية. الرجاء المحاولة مرة أخرى.", chat_id=message.chat.id, message_id=waiting_msg.message_id)
                
    except Exception as e:
        logger.error(f"Error: {e}")
        bot.reply_to(message, "❌ حدث خطأ أثناء المعالجة.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
