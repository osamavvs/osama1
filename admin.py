from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

ADMIN_ID = 8074717568  # ضع الآيدي الخاص بك هنا

def get_admin_markup():
    """أزرار لوحة تحكم الأدمن"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="📊 إحصائيات البوت", callback_data="admin_stats"))
    markup.add(InlineKeyboardButton(text="📢 إرسال رسالة للكل", callback_data="admin_broadcast"))
    markup.add(InlineKeyboardButton(text="⚙️ حالة السيرفرات", callback_data="admin_servers"))
    return markup

def is_admin(user_id):
    return user_id == ADMIN_ID
