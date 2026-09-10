import os
import requests

# Exact URL to monitor
URL_TO_CHECK = "https://smp.upm.edu.my"

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing credentials.")
        return
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(api_url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def main():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        # 10s timeout: portals usually hang when overwhelmed
        response = requests.get(URL_TO_CHECK, headers=headers, timeout=10)
        
        # Check for HTTP 200 OK
        if response.status_code == 200:
            print("Status: UP (200 OK)")
            # Portal is live! Send alert with direct clickable link
            send_telegram(f"🚀 UPM Portal is ONLINE and accessible!\n🔗 {URL_TO_CHECK}")
        else:
            print(f"Status: Server Error ({response.status_code})")
            
    except requests.RequestException as e:
        print(f"Status: Unresponsive / Down ({e})")

if __name__ == "__main__":
    main()