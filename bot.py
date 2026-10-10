    try:
        response = model.generate_content(user_message)
        reply_text = response.text
        if reply_text:
            await update.message.reply_text(reply_text)
    except Exception as e:
        # Error တက်ရင် တကယ့်အကြောင်းရင်းကို ဘော့တ်က ပြန်ပြောစေရန်
        print(f"Error occurred: {e}")
        await update.message.reply_text(f"Error: {e}")
      
