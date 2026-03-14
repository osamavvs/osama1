# main.py
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# تعريف البوت واستخدام مجلد plugins لتنظيم الأوامر
app = Client(
    "GuardBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins") # هذا السطر سيجعل البوت يقرأ الأوامر من مجلد خاص
)

if __name__ == "__main__":
    print("--- البوت بدأ العمل بنجاح ---")
    app.run()
