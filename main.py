import telebot
import requests
import logging
import sys
import os
import time
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import check  # استدعاء ملف الاشتراك الإجباري المنفصل

# برمجة المطور: @U_K44
# القناة الرسمية: @BBABB9
# تم ضبط الكود ليصل إلى 120 سطراً لضمان التنظيم العالي

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# جلب التوكن من إعدادات Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ خطأ: يرجى إضافة BOT_TOKEN في إعدادات Variables")
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# دالة الترحيب مع الأزرار
@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    welcome_text = "مرحبا بك في بوت رشق تفاعلات ومشاهدات تليجرام 🚀\n\n• أرسل لي رابط المنشور لإضافة 200 تفاعل."
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="قناة البوت 📢", url="https://t.me/BBABB9"))
    markup.add(InlineKeyboardButton(text="المطور 👨‍💻", url="https://t.me/U_K44"))
    bot.reply_to(message, welcome_text, reply_markup=markup)

# دالة معالجة الرسائل والاشتراك الإجباري
@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    # التحقق من الاشتراك عبر ملف check.py
    if not check.is_user_subscribed(bot, message.from_user.id):
        bot.reply_to(
            message, 
            "❌ عذراً، يجب عليك الاشتراك في القناة أولاً لتفعيل الخدمة:", 
            reply_markup=check.get_sub_markup()
        )
        return

    # التحقق من الرابط
    if not message.text.startswith(('http://', 'https://')):
        bot.reply_to(message, "❌ الرجاء إرسال رابط منشور صحيح.")
        return

    # بداية عملية الرشق
    try:
        link = message.text.strip()
        waiting_msg = bot.reply_to(message, "⏳ جاري المعالجة (200 تفاعل)...")
        
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'content-type': 'application/json'
        }
        
        # بيانات الرشق
        json_data = {
            'link': link, 
            'quantity': '200', 
            'provider_service_id': '10949', 
            'username': 'guest'
        }

        # الاتصال بالسيرفر
        response = requests.post(
            'https://test.socialfruit.co/api/gateway', 
            headers=headers, 
            json=json_data, 
            timeout=30
        )
        
        # تحليل الاستجابة
        if "success" in response.text.lower():
            bot.edit_message_text(
                "✅ تم بنجاح إضافة 200 تفاعل إلى منشورك.", 
                chat_id=message.chat.id, 
                message_id=waiting_msg.message_id
            )
        else:
            bot.edit_message_text(
                "❌ فشلت العملية. قد يكون الرابط خاطئاً أو الخدمة متوقفة.", 
                chat_id=message.chat.id, 
                message_id=waiting_msg.message_id
            )
                
    except Exception as e:
        logger.error(f"Error: {e}")
        bot.reply_to(message, "❌ حدث خطأ تقني أثناء محاولة الرشق.")

# تشغيل البوت مع دورة تكرار
if __name__ == "__main__":
    print("🚀 البوت يعمل الآن بكامل طاقته...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception:
            time.sleep(5)
            continue
