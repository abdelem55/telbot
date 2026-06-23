import os
import sys
import subprocess

# --- 1. التثبيت التلقائي للمكتبات ---
def install_dependencies():
    required = ["requests", "beautifulsoup4"]
    for lib in required:
        try:
            __import__(lib.replace("beautifulsoup4", "bs4"))
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", lib])

install_dependencies()

import time
import requests
from bs4 import BeautifulSoup

# --- 2. الإعدادات ---
TOKEN = "6767377177:AAEw_qkCMmUfeeakSrTqugd3b96eK59a3c4"
CHAT_ID = "5623578870"

TARGET_PAGES = [
    "https://bingotingo.com/best-social-media-platforms/",
    "https://infoxp.com/canva-pro-invite-link/",
    "https://techedubyte.com/how-to-get-canva-pro-for-free/"
]

# ذاكرة البوت لحفظ آخر رابط تم إرساله من كل موقع لمنع تكرار الروابط الميتة
last_sent_links = {}

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, json=payload, timeout=15)
    except Exception as e:
        print(f"Error: {e}")

def scrape_live_links():
    print("🔄 Scanning for FRESH & NEW Canva Pro links...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    for url in TARGET_PAGES:
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                all_links = soup.find_all('a', href=True)
                
                for link in all_links:
                    href = link['href']
                    
                    if "canva.com" in href and "join" in href:
                        # الحصول على الرابط القديم المخزن لهذا الموقع تحديداً
                        previous_link = last_sent_links.get(url)
                        
                        # شرط صارم: لا ترسل الرابط إلا إذا كان "جديداً ومختلفاً" عن آخر رابط أرسلناه من هذا الموقع
                        if href != previous_link:
                            
                            message = (
                                f"🔥 ✨ *⚠️ FRESH CANVA PRO LINK DETECTED!* ✨ 🔥\n\n"
                                f"📢 *Status:* This is a newly updated team link!\n\n"
                                f"🔗 [Click Here to Join the New Team]({href})\n\n"
                                f"⏱ _Note: Teams fill up within 10-15 minutes of update, act fast!_"
                            )
                            
                            send_telegram_message(message)
                            # تحديث الذاكرة بالرابط الجديد
                            last_sent_links[url] = href
                            time.sleep(2)
                            break # نكتفي بأول رابط جديد نLetterه في الصفحة
        except Exception as e:
            print(f"Error scanning {url}: {e}")

if __name__ == "__main__":
    print("🚀 Fresh Canva Filter Bot is running...")
    send_telegram_message("📡 *Canva Filter Bot:* Started. I will only alert you when a link is UPDATED or CHANGED on the websites.")
    
    while True:
        scrape_live_links()
        # فحص كل 10 دقائق (600 ثانية) لصيد التحديث فور حدوثه
        time.sleep(600)
