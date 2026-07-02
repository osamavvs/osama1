import telebot
import requests
import logging
import sys
import time
import os
from telebot.types import Message

# برمجة @oosss44
# قناة ملفات بوتات مجانيه @X5HDO

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# قراءة التوكن من متغيرات البيئة في Railway لضمان الأمان
BOT_TOKEN = os.getenv("8721155986:AAHdipR_Xg6YUebhq_FWU3_oeHjyNdePT_c")

if not BOT_TOKEN:
    print("❌ خطأ: يرجى إضافة BOT_TOKEN في إعدادات Variables على Railway")
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

def handle_exception(exception, message=None):
    error_msg = f"{str(exception)}"
    logger.error(error_msg, exc_info=True)
    
    if message:
        try:
            bot.reply_to(message, "❌ عذراً، حدث خطأ غير متوقع. الرجاء المحاولة مرة أخرى لاحقاً.")
        except:
            pass

@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    try:
        bot.reply_to(message, "مرحبا بك في بوت رشق تفاعلات ومشاهدات بوست تليجرام مجانا \n\n• أرسل لي رابط المنشور لإضافة تفاعلات.")
    except Exception as e:
        handle_exception(e, message)

@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    try:
        if not message.text.startswith(('http://', 'https://')):
            bot.reply_to(message, "❌ الرجاء إرسال رابط صحيح يبدأ بـ http:// أو https://")
            return

        oosss44 = message.text.strip()
        waiting_msg = bot.reply_to(message, "⏳ جاري معالجة طلبك...")
        
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'ar',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://tgpanel.org',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://tgpanel.org/',
            'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'daVTOOL': 'oosss44',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
            'x-panel-origin': 'https://tgpanel.org',
            'x-panel-referer': 'https://tgpanel.org/free-telegram-reaction',
        }

        json_data = {
            'link': oosss44,
            'quantity': '50',
            'provider_service_id': '10949',
            'username': 'guest',
        }

        try:
            response = requests.post(
                'https://test.socialfruit.co/api/gateway', 
                headers=headers, 
                json=json_data,
                timeout=30
            )
            response.raise_for_status()
            
            if "success" in response.text.lower():
                bot.edit_message_text(
                    "✅ تم بنجاح إضافة التفاعلات",
                    chat_id=message.chat.id,
                    message_id=waiting_msg.message_id
                )
            else:
                bot.edit_message_text(
                    f"❌ فشلت العملية. الرجاء المحاولة مرة أخرى.",
                    chat_id=message.chat.id,
                    message_id=waiting_msg.message_id
                )
                logger.error(f"{response.text}")
                
        except requests.exceptions.Timeout:
            bot.edit_message_text(
                "❌ انتهت مهلة الطلب. الرجاء المحاولة مرة أخرى.",
                chat_id=message.chat.id,
                message_id=waiting_msg.message_id
            )
            
        except requests.exceptions.RequestException as e:
            bot.edit_message_text(
                "❌ فشل الاتصال بالخادم. الرجاء المحاولة مرة أخرى.",
                chat_id=message.chat.id,
                message_id=waiting_msg.message_id
            )
            
    except Exception as e:
        handle_exception(e, message)

if __name__ == "__main__":
    print("🚀 البوت يعمل الآن...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            logger.error(f"{str(e)}", exc_info=True)
            time.sleep(5)
            continue
