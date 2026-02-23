import os
import telebot
from flask import Flask, request

# ۱. اطلاعات اصلی ربات سوم
BOT_TOKEN = "8789321244:AAH3w5NKEmpHAGyxSyryl_3ismAsb4LaYKc"
RENDER_URL = "https://my-bot-3-92df.onrender.com" 

# لیست صاحبان ربات (فقط این یوزرنیم‌ها حق استفاده دارند)
ALLOWED_ADMINS = ['sahar143', 'OYB1234']

# لیست ری‌اکشن‌های درخواستی شما
REACTIONS = ['😢', '🌚', '🍓', '🍾'] 
current_index = 0

bot = telebot.TeleBot(BOT_TOKEN, threaded=True)
app = Flask(__name__)

# لیست تمام فرمت‌ها برای ری‌اکشن زدن روی همه چیز
ALL_TYPES = ['photo', 'video', 'sticker', 'audio', 'animation', 'text', 'voice', 'video_note']

@app.route('/')
def home(): return "Bot 3 is Running Fast!", 200

@app.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    return "Forbidden", 403

# این بخش مخصوص ری‌اکشن زدن در کانال است
@bot.channel_post_handler(content_types=ALL_TYPES)
def handle_channel_posts(message):
    global current_index
    try:
        # ربات روی تمام پست‌های کانالی که در آن ادمین است ری‌اکشن می‌زند
        bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reaction=[telebot.types.ReactionTypeEmoji(REACTIONS[current_index])]
        )
        # تغییر ایموجی برای پست بعدی
        current_index = (current_index + 1) % len(REACTIONS)
    except Exception as e:
        print(f"Channel Reaction Error: {e}")

# این بخش برای جلوگیری از استفاده دیگران در گروه‌ها
@bot.message_handler(content_types=ALL_TYPES)
def handle_group_messages(message):
    global current_index
    try:
        user = message.from_user.username if message.from_user else None
        # فقط اگر یکی از شما دو نفر پیامی بفرستید، ربات ری‌اکشن می‌زند
        if user and user.lower() in [admin.lower() for admin in ALLOWED_ADMINS]:
            bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[telebot.types.ReactionTypeEmoji(REACTIONS[current_index])]
            )
            current_index = (current_index + 1) % len(REACTIONS)
    except Exception as e:
        print(f"Group/Private Error: {e}")

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_URL}/{BOT_TOKEN}")
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

