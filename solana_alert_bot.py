import requests
import time
import random

# إعدادات تليجرام
TELEGRAM_BOT_TOKEN = "7622219142:AAFDK9pu_03jT8Ec3I10Y1OSmMeS1M3qd48"
TELEGRAM_CHAT_ID = "2094695016"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Telegram Error:", e)

# مصادر البيانات
def fetch_from_pumpfun():
    try:
        res = requests.get("https://client-api.pump.fun/v1/tokens/recent", timeout=10)
        return res.json()["results"]
    except:
        return None

def fetch_from_birdeye():
    try:
        url = "https://public-api.birdeye.so/public/tokenlist?limit=20&offset=0"
        headers = {"X-API-KEY": "public"}
        res = requests.get(url, headers=headers, timeout=10)
        return res.json()["data"]["tokens"]
    except:
        return None

def fetch_from_dexscreener():
    try:
        res = requests.get("https://api.dexscreener.com/latest/dex/pairs/solana", timeout=10)
        return res.json()["pairs"]
    except:
        return None

def get_token_list():
    data = fetch_from_pumpfun()
    if data: return parse_pumpfun(data)

    data = fetch_from_birdeye()
    if data: return parse_birdeye(data)

    data = fetch_from_dexscreener()
    if data: return parse_dexscreener(data)

    return []

def parse_pumpfun(data):
    tokens = []
    for token in data:
        tokens.append({
            "name": token.get("name"),
            "symbol": token.get("symbol"),
            "address": token.get("address")
        })
    return tokens

def parse_birdeye(data):
    tokens = []
    for token in data:
        tokens.append({
            "name": token.get("name"),
            "symbol": token.get("symbol"),
            "address": token.get("address")
        })
    return tokens

def parse_dexscreener(data):
    tokens = []
    for token in data:
        tokens.append({
            "name": token.get("baseToken", {}).get("name"),
            "symbol": token.get("baseToken", {}).get("symbol"),
            "address": token.get("pairAddress")
        })
    return tokens

# تخزين العناوين لمنع التكرار
sent_tokens = set()

def main():
    while True:
        tokens = get_token_list()
        for token in tokens:
            address = token["address"]
            if address and address not in sent_tokens:
                sent_tokens.add(address)
                name = token.get("name", "No Name")
                symbol = token.get("symbol", "")
                msg = f"توكن جديد على سولانا 🚀🚀\n\nName: {name}\nSymbol: {symbol}\nAddress: {address}"
                print(msg)
                send_telegram_message(msg)
        time.sleep(30 + random.randint(5, 10))

if __name__ == "__main__":
    main()
