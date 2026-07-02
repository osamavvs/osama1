import telebot
import requests
import os
from telebot.types import Message

# برمجة @U_K44
# قناة ملفات بوتات مجانيه @BBABB9

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    welcome_text = "مرحبا بك في بوت رشق تفاعلات ومشاهدات بوست تليجرام مجانا\n\n"
    welcome_text += "• المطور: @U_K44\n• القناة: @BBABB9\n\n"
    welcome_text += "• أرسل لي رابط المنشور لإضافة تفاعلات."
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    if not message.text.startswith('http'):
        bot.reply_to(message, "❌ الرجاء إرسال رابط صحيح يبدأ بـ http أو https")
        return

    waiting_msg = bot.reply_to(message, "⏳ جاري معالجة طلبك...")
    
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'content-type': 'application/json'
    }

    json_data = {
        'link': message.text.strip(),
        'quantity': '50',
        'provider_service_id': '10949',
        'username': 'guest',
    }

    try:
        response = requests.post('https://test.socialfruit.co/api/gateway', headers=headers, json=json_data, timeout=20)
        
        if "success" in response.text.lower():
            bot.edit_message_text(
                "✅ تم بنجاح إضافة التفاعلات", 
                chat_id=message.chat.id, 
                message_id=waiting_msg.message_id
            )
        else:
            bot.edit_message_text(
                "❌ فشلت العملية. الرجاء المحاولة مرة أخرى.", 
                chat_id=message.chat.id, 
                message_id=waiting_msg.message_id
            )
                
    except Exception:
        bot.edit_message_text(
            "❌ حدث خطأ أثناء المعالجة.", 
            chat_id=message.chat.id, 
            message_id=waiting_msg.message_id
        )

if __name__ == "__main__":
    bot.remove_webhook()
    bot.polling(none_stop=True)
