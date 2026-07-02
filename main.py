import telebot
import requests
import logging
import sys
import time
import os
import random
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# برمجة @U_K44 | قناة @BBABB9

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN)
CHANNEL_ID = "@BBABB9"
last_usage = {} # لحماية البوت من التكرار السريع

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    if not check_subscription(message.from_user.id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="اضغط هنا للاشتراك 📢", url="https://t.me/BBABB9"))
        bot.reply_to(message, "❌ يجب الاشتراك في القناة أولاً:", reply_markup=markup)
        return

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="قناة البوت 📢", url="https://t.me/BBABB9"))
    markup.add(InlineKeyboardButton(text="المطور 👨‍💻", url="https://t.me/U_K44"))
    bot.reply_to(message, "مرحبا بك! أرسل رابط المنشور للرشق (200 تفاعل).", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    # 1. التحقق من الاشتراك
    if not check_subscription(message.from_user.id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="اشترك أولاً 📢", url="https://t.me/BBABB9"))
        bot.reply_to(message, "❌ عذراً، يجب الاشتراك أولاً:", reply_markup=markup)
        return

    # 2. الحماية من الرشق المتكرر (فاصل 300 ثانية - 5 دقائق)
    user_id = message.from_user.id
    if user_id in last_usage and (time.time() - last_usage[user_id] < 300):
        bot.reply_to(message, "⚠️ يرجى الانتظار 5 دقائق بين كل عملية رشق وأخرى.")
        return

    try:
        if not message.text.startswith(('http://', 'https://')):
            bot.reply_to(message, "❌ أرسل رابطاً صحيحاً.")
            return

        waiting_msg = bot.reply_to(message, "⏳ جاري المعالجة...")
        
        # 3. تأخير عشوائي وتغيير الـ User-Agent للتمويه
        time.sleep(random.randint(5, 10))
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        ]
        
        headers = {
            'user-agent': random.choice(user_agents),
            'content-type': 'application/json'
        }

        json_data = {'link': message.text.strip(), 'quantity': '200', 'provider_service_id': '10949', 'username': 'guest'}

        response = requests.post('https://test.socialfruit.co/api/gateway', headers=headers, json=json_data, timeout=30)
        
        if "success" in response.text.lower():
            last_usage[user_id] = time.time() # تسجيل وقت العملية الناجحة
            bot.edit_message_text("✅ تم بنجاح!", chat_id=message.chat.id, message_id=waiting_msg.message_id)
        else:
            bot.edit_message_text("❌ فشلت العملية. السيرفر مشغول حالياً.", chat_id=message.chat.id, message_id=waiting_msg.message_id)
                
    except Exception as e:
        logger.error(f"Error: {e}")
        bot.reply_to(message, "❌ حدث خطأ.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
