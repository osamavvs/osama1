# plugins/commands.py
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions

# 1. الترحيب بالأعضاء
@Client.on_message(filters.new_chat_members)
async def welcome(client, message):
    for member in message.new_chat_members:
        await message.reply_text(f"مرحباً {member.mention}، نورت المجموعة!")

# 2. فلتر الروابط
@Client.on_message(filters.text & filters.group & ~filters.me)
async def delete_links(client, message):
    if "http" in message.text or "t.me/" in message.text:
        await message.delete()
        await message.reply_text(f"عذراً {message.from_user.mention}، الروابط ممنوعة!")

# 3. أمر الكتم (للمشرفين)
@Client.on_message(filters.command("كتم") & filters.group)
async def mute(client, message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in ("administrator", "creator"):
        if message.reply_to_message:
            await client.restrict_chat_member(
                message.chat.id,
                message.reply_to_message.from_user.id,
                ChatPermissions(can_send_messages=False)
            )
            await message.reply_text("تم كتم العضو.")
        else:
            await message.reply_text("رد على رسالة الشخص لكتمه.")
