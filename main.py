import telebot
import requests
import logging
import sys
import time
import os
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# برمجة @U_K44
# قناة ملفات بوتات مجانيه @BBABB9

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ خطأ: يرجى إضافة BOT_TOKEN في إعدادات Variables على Railway")
    sys.exit(1)

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
    welcome_text = "مرحبا بك في بوت رشق تفاعلات ومشاهدات بوست تليجرام مجانا 🚀\n\n"
    welcome_text += "• أرسل لي رابط المنشور لإضافة تفاعلات."
    
    # إنشاء أزرار الإنلاين (معلومات المطور والقناة)
    markup = InlineKeyboardMarkup()
    btn_channel = InlineKeyboardButton(text="قناة البوت 📢", url="https://t.me/BBABB9")
    btn_dev = InlineKeyboardButton(text="المطور 👨‍💻", url="https://t.me/U_K44")
    
    # إضافة الأزرار (كل زر في سطر، أو يمكنك وضع markup.add(btn_channel, btn_dev) ليكونوا بجانب بعض)
    markup.add(btn_channel)
    markup.add(btn_dev)

    bot.reply_to(message, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['dev'])
def send_dev_info(message: Message):
    dev_text = "⚙️ **معلومات المطور:**\n• المطور: @U_K44\n• الأيدي: 8074717568\n• القناة: @BBABB9"
    bot.reply_to(message, dev_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    # التحقق من الاشتراك الإجباري مع زر إنلاين
    if not check_subscription(message.from_user.id):
        markup = InlineKeyboardMarkup()
        btn_sub = InlineKeyboardButton(text="اضغط هنا للاشتراك 📢", url="https://t.me/BBABB9")
        markup.add(btn_sub)
        
        bot.reply_to(message, "❌ عذراً، يجب عليك الاشتراك في القناة أولاً لاستخدام البوت.", reply_markup=markup)
        return

    try:
        if not message.text.startswith(('http://', 'https://')):
            bot.reply_to(message, "❌ الرجاء إرسال رابط صحيح يبدأ بـ http:// أو https://")
            return

        oosss44 = message.text.strip()
        waiting_msg = bot.reply_to(message, "⏳ جاري معالجة طلبك...")
        
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'ar',
            'content-type': 'application/json',
            'origin': 'https://tgpanel.org',
            'referer': 'https://tgpanel.org/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        }

        json_data = {
            'link': oosss44,
            'quantity': '50',
            'provider_service_id': '10949',
            'username': 'guest',
        }

        response = requests.post('https://test.socialfruit.co/api/gateway', headers=headers, json=json_data, timeout=30)
        
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
                
    except Exception as e:
        logger.error(f"Error: {e}")
        bot.reply_to(message, "❌ حدث خطأ أثناء المعالجة.")

if __name__ == "__main__":
    print("🚀 البوت يعمل الآن...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            time.sleep(5)
            continue
