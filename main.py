import telebot
import requests
import logging
import sys
import time
import os
import random
import admin
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN: sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN)
CHANNEL_ID = "@BBABB9"
user_last_usage = {}
user_ids = set() # لتخزين المستخدمين للإذاعة
SERVERS = ['10949', '10950', '10951', '10948']

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except: return False

@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    user_ids.add(message.from_user.id) # حفظ المستخدم للإذاعة
    if not check_subscription(message.from_user.id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="اشترك بالقناة 📢", url="https://t.me/BBABB9"))
        bot.reply_to(message, "❌ يجب الاشتراك أولاً:", reply_markup=markup)
        return
    bot.reply_to(message, "مرحبا! أرسل رابط المنشور للرشق (عليك الانتظار 10 دقائق بين كل عملية).")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if admin.is_admin(message.from_user.id):
        bot.reply_to(message, "👑 لوحة تحكم الأدمن:", reply_markup=admin.get_admin_markup())

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "admin_stats":
        bot.answer_callback_query(call.id, f"عدد المستخدمين: {len(user_ids)}")
    elif call.data == "admin_broadcast":
        bot.edit_message_text("أرسل الرسالة التي تريد إذاعتها للجميع:", call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(call.message, broadcast_process)
    elif call.data == "admin_servers":
        bot.answer_callback_query(call.id, "السيرفرات نشطة")

def broadcast_process(message):
    for uid in user_ids:
        try: bot.send_message(uid, message.text)
        except: continue
    bot.reply_to(message, "✅ تمت الإذاعة بنجاح.")

@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    if not check_subscription(message.from_user.id): return
    
    user_id = message.from_user.id
    current_time = time.time()
    # نظام الانتظار 10 دقائق (600 ثانية)
    if user_id in user_last_usage and (current_time - user_last_usage[user_id] < 600):
        bot.reply_to(message, "⚠️ انتظر 10 دقائق بين كل عملية.")
        return
    
    try:
        waiting_msg = bot.reply_to(message, "⏳ جاري المعالجة...")
        headers = {'user-agent': 'Mozilla/5.0', 'content-type': 'application/json'}
        json_data = {'link': message.text.strip(), 'quantity': '200', 'provider_service_id': random.choice(SERVERS), 'username': 'guest'}
        
        response = requests.post('https://test.socialfruit.co/api/gateway', headers=headers, json=json_data, timeout=30)
        
        # كشف سبب الفشل الحقيقي
        if response.status_code == 200 and "success" in response.text.lower():
            user_last_usage[user_id] = time.time()
            bot.edit_message_text("✅ تم بنجاح!", chat_id=message.chat.id, message_id=waiting_msg.message_id)
        else:
            bot.edit_message_text(f"❌ فشل: {response.status_code}", chat_id=message.chat.id, message_id=waiting_msg.message_id)
            logger.error(f"Error: {response.text}")
    except Exception as e:
        bot.reply_to(message, "❌ خطأ.")

if __name__ == "__main__":
    while True:
        try: bot.polling(none_stop=True, timeout=60)
        except: time.sleep(10)
