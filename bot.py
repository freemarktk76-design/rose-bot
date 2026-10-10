import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

# Logging သတ်မှတ်ခြင်း
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# OpenAI API client တည်ဆောက်ခြင်း (Railway ထဲက Environment Variable မှ ယူပါမည်)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    if not user_message:
        return

    # Typing status ပြသခြင်း
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # OpenAI ChatGPT သို့ စာပို့ပြီး အဖြေထုတ်ခြင်း
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant named Rose."},
                {"role": "user", "content": user_message}
            ]
        )
        reply_text = response.choices[0].message.content
    except Exception as e:
        reply_text = "ဝမ်းနည်းပါတယ်၊ လက်ရှိတွင် အမှားအယွင်း အချို့ရှိနေပါသည်။"

    await update.message.reply_text(reply_text)

if __name__ == '__main__':
    # Telegram Bot Token ကို Railway ထဲက Environment Variable မှ ယူပါမည်
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # မက်ဆေ့ခ်ျအားလုံးကို လက်ခံရယူရန် Handler ထည့်ခြင်း
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is running...")
    app.run_polling()
    
