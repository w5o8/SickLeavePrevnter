import telebot
from telebot.types import ChatPermissions
import re
TOKEN = 'ROKEN'
bot = telebot.TeleBot(TOKEN)
alert = '''
    تم إسكات أحد الأعضاء. يُرجى مراجعة الأحداث المتعلقة بهذا الإجراء واتخاذ القرار المناسب تجاهه.
    @x7mdNet @Kleja @HamzaIT2
    '''
PROHIBITED_WORDS = [
    ["سكليف"],
    ["صحتي", "مرضية"]
]
def clean_message(message):
    message_text = message.text
    PROHIBITED = r'[+=\-!@#$%^&*()ـ.,،/ـ\u064e\u064f\u0650\u0652\u0651\u064b\u064c\u064d]'
    cleaned_message = re.sub(PROHIBITED, '', message_text)
    return cleaned_message
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,'Add me to prevent Sick Leave in ARABIC')

@bot.message_handler(func=lambda message:True)
def handle_messages(message):
    permissions = ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False,
        can_change_info=False,
        can_invite_users=False,
        can_pin_messages=False
    )
    cleaned_message = clean_message(message)
    member_id = message.from_user.id
    chat_member = bot.get_chat_member(chat_id=message.chat.id, user_id=member_id)
    if chat_member.status not in ['administrator', 'creator']:
        for arr in PROHIBITED_WORDS:
            if all(word in cleaned_message for word in arr):

                try:
                    bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
                    bot.restrict_chat_member(chat_id=message.chat.id, user_id=member_id, permissions=permissions)
                    bot.send_message(chat_id=message.chat.id,text=alert)
                except Exception as e:
                        print("حصل خطأ")


bot.infinity_polling()
