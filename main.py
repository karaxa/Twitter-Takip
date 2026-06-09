import feedparser
import requests
import os

RSS_URL = "https://nitter.net/Adememrem1/rss"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# En son gönderilen tweetin ID'sini saklamak için bir dosya
LAST_ID_FILE = "last_id.txt"

def get_last_id():
    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE, "r") as f: return f.read().strip()
    return ""

def save_last_id(id):
    with open(LAST_ID_FILE, "w") as f: f.write(id)

feed = feedparser.parse(RSS_URL)
last_id = get_last_id()

feed = feedparser.parse(RSS_URL)
print(f"Feed icerigi: {len(feed.entries)} tweet bulundu.") # Bunu ekle
last_id = get_last_id()

if feed.entries:
    newest_tweet = feed.entries[0]
    
    if newest_tweet.id != last_id:
        # Telegram'a gönder
        print(f"Tetikleme basarili! Yeni tweet tespit edildi: {newest_tweet.id}")
        msg = f"Yeni Tweet: {newest_tweet.title}\n{newest_tweet.link}"
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
        save_last_id(newest_tweet.id)
    else:
        # Tweet yoksa sessizce çık
        print("Yeni tweet yok, tetikleyici bekleniyor.")
else:
    print("RSS kaynaginda hic tweet bulunamadi!")
    
