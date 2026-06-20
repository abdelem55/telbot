import time
import requests
import feedparser

# --- إعدادات التليجرام (ضع بياناتك هنا) ---
TOKEN = "6767377177:AAEw_qkCMmUfeeakSrTqugd3b96eK59a3c4"
CHAT_ID = "5623578870"

# --- قائمة المصادر (RSS Feeds) ---
SOURCES = {
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    "Exploit-DB": "https://www.exploit-db.com/rss.xml",
    "Packet Storm": "https://rss.packetstormsecurity.com/news/"
}

# قائمة لتخزين الروابط المرسلة سابقاً حتى لا تتكرر الأخبار
sent_articles = set()

def send_telegram_message(text):
    """دالة إرسال الرسائل إلى تليجرام"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

def check_news():
    """دالة فحص المصادر وجلب الجديد"""
    print("Checking for new updates...")
    for source_name, url in SOURCES.items():
        try:
            feed = feedparser.parse(url)
            # نأخذ آخر 3 أخبار فقط من كل مصدر في كل جولة فحص
            for entry in feed.entries[:3]:
                link = entry.link
                
                # إذا كان الخبر لم يرسل من قبل
                if link not in sent_articles:
                    title = entry.title
                    
                    # صياغة الرسالة
                    message = f"🚨 *{source_name}* 🚨\n\n📌 *Title:* {title}\n\n🔗 [Read More]({link})"
                    
                    send_telegram_message(message)
                    sent_articles.add(link)
                    time.sleep(2) # تأخير بسيط لتجنب الحظر من تليجرام
        except Exception as e:
            print(f"Error parsing {source_name}: {e}")

# --- تشغيل البوت بشكل مستمر ---
if __name__ == "__main__":
    print("Bot is running...")
    while True:
        check_news()
        # انتظر ساعة كاملة (3600 ثانية) قبل الفحص المرة القادمة
        time.sleep(3600)
