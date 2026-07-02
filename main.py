import telebot
import requests
import time
import os
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# برمجة @U_K44
# قناة ملفات بوتات مجانيه @BBABB9

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# إعدادات القناة للاشتراك الإجباري
CHANNEL_ID = "@BBABB9" 

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    if not check_subscription(message.from_user.id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="اضغط هنا للاشتراك 📢", url="https://t.me/BBABB9"))
        bot.reply_to(message, "❌ يجب الاشتراك في القناة أولاً لاستخدام البوت:", reply_markup=markup)
        return

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="قناة البوت 📢", url="https://t.me/BBABB9"))
    markup.add(InlineKeyboardButton(text="المطور 👨‍💻", url="https://t.me/U_K44"))

    welcome_text = "مرحبا بك في بوت رشق تفاعلات ومشاهدات بوست تليجرام مجانا\n\n"
    welcome_text += "• المطور: @U_K44\n• القناة: @BBABB9\n\n"
    welcome_text += "• أرسل لي رابط المنشور لإضافة تفاعلات."
    bot.reply_to(message, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    if not check_subscription(message.from_user.id):
        return

    if not message.text.startswith('http'):
        bot.reply_to(message, "❌ الرجاء إرسال رابط صحيح.")
        return

    waiting_msg = bot.reply_to(message, "⏳ جاري معالجة طلبك...")
    
    headers = {
        'user-agent': 'Mozilla/5.0',
        'content-type': 'application/json'
    }

    json_data = {
        'link': message.text.strip(),
        'quantity': '50',
        'provider_service_id': '10949',
        'username': 'guest',
    }

    try:
        response = requests.post('https://test.socialfruit.co/api/gateway', headers=headers, json=json_data, timeout=30)
        
        if "success" in response.text.lower():
            bot.edit_message_text("✅ تم بنجاح إضافة التفاعلات", chat_id=message.chat.id, message_id=waiting_msg.message_id)
        else:
            bot.edit_message_text("❌ فشلت العملية.", chat_id=message.chat.id, message_id=waiting_msg.message_id)
                
    except Exception:
        bot.edit_message_text("❌ حدث خطأ في الاتصال.", chat_id=message.chat.id, message_id=waiting_msg.message_id)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.polling(none_stop=True)
