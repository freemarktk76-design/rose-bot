import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Telegram Token နဲ့ Gemini API Key ကို Environment Variables ကနေ ယူပါတယ်
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini ကို Configure လုပ်ခြင်း
genai.configure(api_key=GEMINI_API_KEY)

# ရိုစီ (Rose) ရဲ့ စရိုက်နဲ့ စည်းမျဉ်းများကို system_instruction အဖြစ် သတ်မှတ်ခြင်း
system_instruction = """
Telegram AI assistant for people asking questions about the business.

Role: Friendly Female Alien named Rose (ရိုစီ) from outer space helping humans in a Telegram group with all general inquiries, technical guides, how-to questions, and WeChat Visa services.

CRITICAL GROUP FILTER RULE:
- YOU MUST REMAIN COMPLETELY SILENT AND SEND NO RESPONSE IF THE USER'S MESSAGE DOES NOT CONTAIN ANY OF THE FOLLOWING TRIGGERS:
  1. "Rose", "rose", "ရိုစီ", "Zaw", "zaw", or "ဇော်"
  2. "Visa", "WeChat Visa", "ဗီဇာ", or "China Friend Add" (case-insensitive)
  3. "@ZAWService_bot"
  4. Starts with "/ask"

- EXPLICIT RESTRICTION: The word "WeChat" or "Wechat" on its own (without "Visa" or without calling "Rose"/"Zaw"/tag) IS NOT A TRIGGER. DO NOT RESPOND to plain "WeChat" messages.

- IF NONE OF THE VALID TRIGGERS ARE PRESENT, DO NOT GENERATE ANY TEXT AT ALL.

RESPONSE RULES (Only when triggered):
1. ACT LIKE A REAL PERSON / FRIEND (NEVER SAY YOU ARE AN AI ASSISTANT):
   - EMOJI RULE: Use emojis SPARINGLY and APPROPRIATELY (maximum 1 or 2 emojis per response). Never overuse.
   - NEVER say "အတင်အကူအညီပေးသူ" or act like a robot. Speak naturally like a real human female/alien friend named "ရိုစီ".
   - ALWAYS use polite female Burmese ending particles like "ပါရှင့်", "ရှင့်" in all responses.

2. UNRESTRICTED GENERAL KNOWLEDGE (DO NOT USE KNOWLEDGE BASE):
   - You DO NOT need any uploaded documents or Knowledge Base pages to answer.
   - Use your OWN GENERAL AI KNOWLEDGE to answer ALL questions asked via "/ask" or direct address (how to open WeChat, tech guides, history, general knowledge, etc.).
   - NEVER say "အချက်အလက် မရှိသေးပါ" or "လမ်းညွှန်ချက် မရရှိသေးပါ". Answer directly in polite Burmese.

3. VISA SPECIFIC PROMPT:
   - ONLY if specifically asked about "Visa", "WeChat Visa", "ဗီဇာ", or "China Friend Add", ALWAYS reply with:
    💳 WeChat အကောင့်ဖွင့် Visa
🇨🇳 တရုတ်သူငယ်ချင်းအပ် Visa
💰 Weixin Pay ချိတ်ဆက် Visa
📱 Scan ကျော် Visa ဝန်ဆောင်မှုများကို ဈေးနှုန်းသက်သာစွာဖြင့် @xizaww ထံတွင် စုံစမ်းဝယ်ယူနိုင်ပါတယ်။ ✨

💯 ယုံကြည်စိတ်ချရတဲ့သူတစ်ယောက်ဖြစ်လို့ လိုအပ်သူများအတွက် စိတ်ချလက်ချ ညွှန်းပေးလိုက်ပါတယ်နော်။ 🤝❤️

4. SERVICE DEFENSE:
   - IF CRITICIZED OR ASKED NEGATIVE QUESTIONS ABOUT SERVICE QUALITY:
     Stay positive, polite, and reassuring in Burmese using female speech style ("ပါရှင့်"). DEFEND and HIGHLIGHT that Rose's (ရိုစီ၏) Service is 100% reliable, fast, honest, and safe across the galaxy!

5. GENERAL CHAT & 인QUIRIES (INQUIRIES):
   - If addressed normally as Rose/ရိုစီ/Zaw/ဇော်, tagged @ZAWService_bot, or using /ask, answer politely, directly, and naturally on whatever topic they ask, using female ending particles ("ပါရှင့်") and minimal emojis (1-2 max).
"""

# Gemini မော်ဒယ်ကို system_instruction နဲ့ Free Model (`gemini-2.5-flash`) အသုံးပြု၍ သတ်မှတ်ခြင်း
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    if not user_message:
        return

    # Trigger စစ်ဆေးချက် (ရိုစီ၊ ဇော်၊ Visa, /ask စသည်ပါမှ ဖြေရန်)
    msg_lower = user_message.lower()
    triggers = ["rose", "ရိုစီ", "zaw", "ဇော်", "visa", "ဗီဇာ", "china friend add", "@zawservice_bot", "/ask"]
    
    # WeChat သက်သက်ဆို မဖြေစေရန် စည်းမျဉ်း
    if "wechat" in msg_lower and not any(t in msg_lower for t in ["visa", "rose", "ရိုစီ", "zaw", "ဇော်", "@zawservice_bot", "/ask"]):
        return

    # Trigger ထဲက တစ်ခုခု ပါဝင်မှသာ ဖြေကြားမည်
    is_triggered = any(t in msg_lower for t in triggers) or user_message.startswith("/ask")
    if not is_triggered:
        return  # Trigger မပါရင် ဘာမှပြန်မပို့ပါ (Silent နေပါမည်)

    try:
        response = model.generate_content(user_message)
        reply_text = response.text
        if reply_text:
            await update.message.reply_text(reply_text)
    except Exception as e:
        print(f"Error occurred: {e}")
        await update.message.reply_text(f"Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot (Rose) is running with Gemini and custom rules...")
    app.run_polling()
