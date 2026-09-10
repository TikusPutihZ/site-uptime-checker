import os
import requests

URL_TO_CHECK = "https://smp.upm.edu.my"

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("ERROR: Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID!", flush=True)
        return

    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(api_url, json=payload, timeout=10)
        print(f"Telegram API Status Code: {response.status_code}", flush=True)
        print(f"Telegram API Response: {response.text}", flush=True)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}", flush=True)

def main():
    print("--- Starting Check ---", flush=True)
    
    # 1. Send a test message immediately to verify Telegram credentials work
    print("Sending bot connection test...", flush=True)
    send_telegram("🔔 Uptime Checker is active and testing bot connection!")

    # 2. Check the website
    print(f"Pinging {URL_TO_CHECK}...", flush=True)
    try:
        response = requests.get(
            URL_TO_CHECK, 
            timeout=15, 
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        print(f"Site response code: {response.status_code}", flush=True)
        
        if response.status_code == 200:
            print("Site is UP!", flush=True)
            send_telegram(f"🟢 The portal is UP and responding (Status 200)!\n{URL_TO_CHECK}")
        else:
            print(f"Site returned error status: {response.status_code}", flush=True)
            send_telegram(f"⚠️ Site responded with HTTP {response.status_code}")
            
    except requests.RequestException as e:
        print(f"Site unreachable / timeout: {e}", flush=True)
        send_telegram(f"🔴 Site is currently unreachable / timed out.")

if __name__ == "__main__":
    main()