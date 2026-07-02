from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

CHANNEL_ID = "@BBABB9" 

def is_user_subscribed(bot, user_id):
    """دالة التحقق من الاشتراك"""
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def get_sub_markup():
    """زر الاشتراك"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="📢 اشترك في القناة لتفعيل البوت", url="https://t.me/BBABB9"))
    return markup

