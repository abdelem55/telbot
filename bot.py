import os
import sys
import subprocess

# --- 1. التثبيت التلقائي للمكتبات لضمان عدم توقف الحاوية ---
def install_dependencies():
    required = ["requests", "feedparser", "beautifulsoup4"]
    for lib in required:
        try:
            __import__(lib.replace("beautifulsoup4", "bs4"))
        except ImportError:
            print(f"📦 Installing {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", lib])

install_dependencies()

import time
import re
import requests
import feedparser
from bs4 import BeautifulSoup

# --- 2. إعدادات التليجرام (ضع بياناتك هنا) ---
TOKEN = "6767377177:AAEw_qkCMmUfeeakSrTqugd3b96eK59a3c4"
CHAT_ID = "5623578870"

# --- 3. مصادر روابط كانفا برو (مدونات تقنية ومنصات تحديث روابط) ---
SOURCES = {
    "Bingo Tingo Updates": "https://bingotingo.com/feed/",
    "Tech Edu Byte": "https://techedubyte.com/feed/",
    "Infoxp": "https://infoxp.com/feed/",
    "Daily Canva Teams": "https://www.alltechbuzz.net/feed/"
}

sent_links = set()

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        requests.post(url, json=payload, timeout=15)
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

def check_canva_links():
    print("🔍 Searching for new Canva Pro Links...")
    for source_name, url in SOURCES.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]: # فحص آخر 5 مقالات
                title = entry.title.lower()
                link = entry.link
                
                # التحقق مما إذا كان المقال يتحدث عن Canva Pro أو Canva Team
                if "canva" in title and link not in sent_links:
                    
                    # صياغة رسالة تنبيهية بالرابط المباشر للمقال الذي يحتوي على الدعوة
                    message = (
                        f"🎨 ✨ *New Canva Pro Link Detected!* ✨ 🎨\n\n"
                        f"📌 *Source:* {source_name}\n"
                        f"📝 *Article:* {entry.title}\n\n"
                        f"🔗 *Get your Link Here:* {link}\n\n"
                        f"⏰ _Hurry up before the team gets full (Max 500 members)!_"
                    )
                    
                    send_telegram_message(message)
                    sent_links.add(link)
                    time.sleep(2)
        except Exception as e:
            print(f"Error checking {source_name}: {e}")

# --- 4. تشغيل البوت ---
if __name__ == "__main__":
    print("🚀 Canva Pro Link Finder Bot is running...")
    while True:
        check_canva_links()
        # فحص كل 30 دقيقة لأن روابط كانفا تمتلئ بسرعة وتغلق
        time.sleep(1800)
