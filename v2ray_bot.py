from telegram.ext import Updater, MessageHandler, Filters
import re, json, os

BOT_TOKEN = "7584460443:AAEXNaLpa8pwDkZI1SiDuat-kgjrhOMl1j4"
OUTPUT_FILE = "v2configs.json"

def extract_configs(text):
    pattern = r"(vmess://[^\s]+|vless://[^\s]+|trojan://[^\s]+|ss://[^\s]+|ssr://[^\s]+)"
    return re.findall(pattern, text)

def handle_message(update, context):
    message = update.message.text
    if not message:
        return

    configs = extract_configs(message)
    if configs:
        print(f"✅ {len(configs)} کانفیگ جدید پیدا شد.")
        save_configs(configs)

def save_configs(new_configs):
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            old_configs = json.load(f)
    else:
        old_configs = []

    all_configs = list(set(old_configs + new_configs))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_configs, f, indent=2, ensure_ascii=False)

    print(f"📦 مجموع کانفیگ‌ها: {len(all_configs)}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & Filters.chat_type.channel, handle_message))

    # ✅ تنظیم Webhook
    APP_URL = "https://v2easy.vercel.app/"  # آدرس Vercel
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        url_path=BOT_TOKEN,
        webhook_url=APP_URL + BOT_TOKEN
    )
    updater.idle()

if __name__ == '__main__':
    main()
