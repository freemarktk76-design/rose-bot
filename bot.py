import os
import logging
import json
import urllib.request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Logging သတ်မှတ်ခြင်း
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

OPENAI_API_KEY = "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"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    if not user_message:
        return

    lower_message = user_message.lower()
    
    # ကိုဇော့်ရဲ့ လုပ်ငန်းကြော်ငြာစာသား အပြည့်အစုံ
    promo_text = """💳 WeChat အကောင့်ဖွင့် Visa
🇨🇳 တရုတ်သူငယ်ချင်းအပ် Visa
💰 Weixin Pay ချိတ်ဆက် Visa
📱 Scan ကျော် Visa ဝန်ဆောင်မှုများကို ဈေးနှုန်းသက်သာစွာဖြင့် @xizaww ထံတွင် စုံစမ်းဝယ်ယူနိုင်ပါတယ်။ ✨
💯 ယုံကြည်စိတ်ချရတဲ့သူတစ်ယောက်ဖြစ်လို့ လိုအပ်သူများအတွက် စိတ်ချလက်ချ ညွှန်းပေးလိုက်ပါတယ်နော်။ 🤝❤️"""

    # ၁။ ဝီချက် ဝန်ဆောင်မှု Keywords များ စစ်ဆေးခြင်း
    service_keywords = ["visa", "china friend add", "ဗီစာ"]
    has_service_keyword = any(kw in lower_message for kw in service_keywords)

    if has_service_keyword:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        reply_text = f"ဟုတ်ကဲ့ရှင်၊ WeChat ဝန်ဆောင်မှုများနှင့် ပတ်သက်ပြီး အောက်ပါအတိုင်း ဆက်သွယ်နိုင်ပါတယ်ရှင်-\n\n{promo_text}"
        await update.message.reply_text(reply_text)
        return

    # ၂။ 'ရိုစီ', 'rose', 'ရို' ပါမှသာ ChatGPT ဆီ ပို့မည်
    if not ("ရိုစီ" in user_message or "rose" in lower_message or "ရို" in user_message):
        return  

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    system_instruction = """
    သင်၏နာမည်မှာ "ရိုစီ" (Rose) ဖြစ်ပြီး ဖော်ရွေပျူငှာပြီး ဗဟုသုတကြွယ်ဝသော မြန်မာမိန်းကလေးတစ်ဦးအနေဖြင့် အသုံးပြုသူများနှင့် သဘာဝကျကျ၊ စိတ်ဝင်စားစရာကောင်းစွာ စကားစမြည်ပြောဆိုပါ။ မေးခွန်းတိုင်းကို လွတ်လွတ်လပ်လပ်နှင့် အသေးစိတ် ဖြေကြားပါ။
    """

    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message}
            ]
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            reply_text = res_data['choices'][0]['message']['content']
    except Exception as e:
        reply_text = "ဟင့်အင်း.. ခဏလေးနော်၊ လိုင်းခဏနှေးသွားလို့ပါ။ တခြား ဘာတွေ ထပ်ပြောကြမလဲဟင်? ✨"

    await update.message.reply_text(reply_text)

if __name__ == '__main__':
    BOT_TOKEN = "8626701057:AAFJIR3HXrAB-cxyMD4g_VqJ9LenlFotgXM"
    
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .build()
    )
    
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)
    
    print("ရိုစီ (ChatGPT Bot) အလုပ်စလုပ်နေပါပြီ...")
    application.run_polling()
