from flask import Flask, request
import requests
import json
import sys
from telegram_config import TELEGRAM_API_KEY, TELEGRAM_CHAT_ID

app = Flask(__name__)

def send_telegram_notification(s):
    hook_url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage"
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    msg_data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': s
    }
    response = requests.post(hook_url, headers=headers, data=json.dumps(msg_data))

    # Debug the response
    if response.status_code == 200:
        print(f"Telegram notification sent successfully: {response.status_code}")
        sys.stdout.flush()
    else:
        print(f"Telegram notification failed with status code: {response.status_code}. Url: {hook_url}")
        print(f"Error message: {response.text}")
        sys.stdout.flush()

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get URL
    url = request.url

    # Get headers
    headers = dict(request.headers)

    # Get POST data
    try:
        post_data = request.get_json(force=True)
    except:
        post_data = request.get_data(as_text=True)

    # Print debug message
    print("=" * 80)
    print("WEBHOOK RECEIVED")
    print("=" * 80)
    print(f"URL: {url}")
    print("-" * 80)
    print("HEADERS:")
    print(json.dumps(headers, indent=2))
    print("-" * 80)
    print("POST DATA:")
    post_data_str = json.dumps(post_data, indent=2) if isinstance(post_data, dict) else post_data
    print(post_data_str)
    print("=" * 80)
    sys.stdout.flush()

    send_telegram_notification(post_data_str)

    return {"status": "ok"}, 200

@app.route('/health', methods=['GET'])
def health():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
