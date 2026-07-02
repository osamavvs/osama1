import telebot
import requests
import logging
import sys
import time
import os
import random
import admin
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# برمجة المطور: @U_K44 | قناة: @BBABB9
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN: sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN)
CHANNEL_ID = "@BBABB9"
user_last_usage = {}
SERVERS = ['10949', '10950', '10951', '10948']

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except: return False

@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    if not check_subscription(message.from_user.id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="اشترك بالقناة 📢", url="https://t.me/BBABB9"))
        bot.reply_to(message, "❌ يجب الاشتراك أولاً:", reply_markup=markup)
        return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="قناة البوت 📢", url="https://t.me/BBABB9"))
    markup.add(InlineKeyboardButton(text="المطور 👨‍💻", url="https://t.me/U_K44"))
    bot.reply_to(message, "مرحبا بك! أرسل رابط المنشور للرشق (200).", reply_markup=markup)

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if admin.is_admin(message.from_user.id):
        bot.reply_to(message, "👑 لوحة التحكم:", reply_markup=admin.get_admin_markup())
    else: bot.reply_to(message, "❌ ليس لديك صلاحيات!")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "admin_stats": bot.answer_callback_query(call.id, "البوت يعمل بكفاءة - @U_K44")
    elif call.data == "admin_servers": bot.answer_callback_query(call.id, f"السيرفرات المتاحة: {len(SERVERS)}")

@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    if not check_subscription(message.from_user.id): return
    
    user_id = message.from_user.id
    current_time = time.time()
    if user_id in user_last_usage and (current_time - user_last_usage[user_id] < 300):
        bot.reply_to(message, "⚠️ انتظر 5 دقائق بين كل عملية.")
        return
    
    try:
        if not message.text.startswith(('http')):
            bot.reply_to(message, "❌ رابط غير صحيح.")
            return
        waiting_msg = bot.reply_to(message, "⏳ جاري المعالجة...")
        
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'content-type': 'application/json'}
        json_data = {'link': message.text.strip(), 'quantity': '200', 'provider_service_id': random.choice(SERVERS), 'username': 'guest'}
        
        response = requests.post('https://test.socialfruit.co/api/gateway', headers=headers, json=json_data, timeout=30)
        
        if response.status_code == 200 and "success" in response.text.lower():
            user_last_usage[user_id] = time.time()
            bot.edit_message_text("✅ تم بنجاح!", chat_id=message.chat.id, message_id=waiting_msg.message_id)
        else:
            bot.edit_message_text("❌ فشلت العملية. حاول لاحقاً.", chat_id=message.chat.id, message_id=waiting_msg.message_id)
    except Exception as e:
        logger.error(f"Error: {e}")
        bot.reply_to(message, "❌ خطأ تقني.")

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
        except Exception as e:
            time.sleep(10)
            continue
