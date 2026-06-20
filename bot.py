import os
import sys
import subprocess

# --- 1. إجبار الحاوية على تثبيت المكتبات الناقصة برمجياً ---
def install_dependencies():
    required_libraries = ["requests", "feedparser"]
    for lib in required_libraries:
        try:
            __import__(lib)
        except ImportError:
            print(f"📦 Library '{lib}' missing. Installing it now...")
            try:
                # تشغيل أمر التثبيت صامتًا لتجنب المشاكل
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", lib])
                print(f"✅ '{lib}' installed successfully!")
            except Exception as e:
                print(f"❌ Failed to install '{lib}': {e}")
                sys.exit(1)

# تشغيل الفحص والتثبيت قبل أي شيء آخر
install_dependencies()

# الآن نقوم باستدعاء المكتبات بأمان بعد التأكد من تثبيتها
import time
import requests
import feedparser

# --- 2. إعدادات التليجرام (ضع بياناتك هنا) ---
TOKEN = "6767377177:AAEw_qkCMmUfeeakSrTqugd3b96eK59a3c4"
CHAT_ID = "5623578870"

# --- 3. قائمة المصادر (RSS Feeds) ---
SOURCES = {
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    "Exploit-DB": "https://www.exploit-db.com/rss.xml",
    "Packet Storm": "https://rss.packetstormsecurity.com/news/"
}

sent_articles = set()

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending message: {e}")

def check_news():
    print("🔍 Checking for new updates...")
    for source_name, url in SOURCES.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                link = entry.link
                if link not in sent_articles:
                    title = entry.title
                    message = f"🚨 *{source_name}* 🚨\n\n📌 *Title:* {title}\n\n🔗 [Read More]({link})"
                    send_telegram_message(message)
                    sent_articles.add(link)
                    time.sleep(2) 
        except Exception as e:
            print(f"Error parsing {source_name}: {e}")

# --- 4. تشغيل البوت ---
if __name__ == "__main__":
    print("🚀 Bot bypass initialized. Ready to fetch cyber security news!")
    while True:
        check_news()
        time.sleep(3600)  # فحص كل ساعة
