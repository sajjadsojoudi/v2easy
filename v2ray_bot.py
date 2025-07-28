from telegram.ext import Updater, MessageHandler, Filters
import re
import json
import os

# 🔐 توکن رباتت رو اینجا بذار
BOT_TOKEN = "7584460443:AAEXNaLpa8pwDkZI1SiDuat-kgjrhOMl1j4"

# 📁 مسیر ذخیره فایل JSON
OUTPUT_FILE = "v2configs.json"

# تابع استخراج لینک‌های کانفیگ از متن پیام
def extract_configs(text):
    pattern = r"(vmess://[^\s]+|vless://[^\s]+|trojan://[^\s]+|ss://[^\s]+|ssr://[^\s]+)"
    return re.findall(pattern, text)

# تابع هندل کردن پیام‌های دریافتی
def handle_message(update, context):
    message = update.message.text
    if not message:
        return

    configs = extract_configs(message)
    if configs:
        print(f"✅ {len(configs)} کانفیگ جدید پیدا شد.")
        save_configs(configs)

# ذخیره کانفیگ‌ها داخل JSON
def save_configs(new_configs):
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            old_configs = json.load(f)
    else:
        old_configs = []

    all_configs = list(set(old_configs + new_configs))  # حذف تکراری‌ها

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_configs, f, indent=2, ensure_ascii=False)

    print(f"📦 مجموع کانفیگ‌ها: {len(all_configs)}")

# اجرای ربات
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & Filters.chat_type.channel, handle_message))

    print("🤖 ربات فعال شد. منتظر پیام‌های کانال‌ها هستیم...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
