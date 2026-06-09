import feedparser
import requests
import os

RSS_URL = "https://nitter.poast.org/Adememrem1/rss"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
LAST_DATE_FILE = "last_date.txt"

def get_last_date():
    if os.path.exists(LAST_DATE_FILE):
        with open(LAST_DATE_FILE, "r") as f: return f.read().strip()
    return ""

def save_last_date(date):
    with open(LAST_DATE_FILE, "w") as f: f.write(date)

feed = feedparser.parse(RSS_URL)
last_date = get_last_date()

if feed.entries:
    newest_tweet = feed.entries[0]
    newest_date = newest_tweet.get('published', '')

    print(f"Kontrol: RSS Tarihi ({newest_date}) vs Kayitli Tarih ({last_date})")

    if newest_date != last_date and newest_date != "":
        print("Yeni tweet bulundu, gonderiliyor...")
        msg = f"Yeni Tweet: {newest_tweet.title}\n{newest_tweet.link}"
        # Telegram'a gönderim
        response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
        print(f"Telegram Yaniti: {response.status_code}") # Hata varsa loglarda görelim
        save_last_date(newest_date)
    else:
        print("Yeni tweet yok (Tarih ayni).")
else:
    print("RSS kaynaginda hic tweet bulunamadi!")
    
