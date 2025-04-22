import requests

TELEGRAM_BOT_TOKEN = '7622219142:AAFDK9pu_03jT8Ec3I10Y1OSmMeS1M3qd48'
TELEGRAM_CHAT_ID = '2094695016'

def send_telegram_alert(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    requests.post(url, data=data)

def fetch_tokens_from_pumpfun():
    print("جاري جلب التوكنات من pump.fun...")
    response = requests.get("https://client-api.pump.fun/v1/tokens/recent")
    if response.status_code == 200:
        return response.json()
    return []

def fetch_token_data_from_dexscreener(token_address):
    print(f"جلب بيانات DexScreener للتوكن: {token_address}")
    url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{token_address}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("pair", {})
    return {}

def analyze_and_alert_once():
    tokens = fetch_tokens_from_pumpfun()
    print(f"عدد التوكنات الجديدة: {len(tokens)}")
    for token in tokens[:3]:
        token_address = token.get("id")
        token_name = token.get("name", "N/A")
        dex_data = fetch_token_data_from_dexscreener(token_address)
        if dex_data:
            price = dex_data.get("priceUsd", "N/A")
            liquidity = dex_data.get("liquidity", {}).get("usd", "N/A")
            market_cap = dex_data.get("fdv", "N/A")
            holders = dex_data.get("holders", "N/A")
            message = f"🚀 توكن جديد على سولانا 🚀\\n" \
                      f"الاسم: {token_name}\\n" \
                      f"العنوان: {token_address}\\n" \
                      f"السعر: {price}$\\n" \
                      f"السيولة: {liquidity}$\\n" \
                      f"ماركت كاب: {market_cap}$\\n" \
                      f"عدد الحائزين: {holders}"
            print(f"إرسال تنبيه للتوكن: {token_name}")
            send_telegram_alert(message)

analyze_and_alert_once()
