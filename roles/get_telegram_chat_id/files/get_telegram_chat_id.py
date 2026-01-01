# Gets telegram chat id. That's necessary to send messages to user
# Chat id should be stored in vars for further runs (to avoid sending a telegram message each time)
import os, requests, sys

api_base_url = "https://api.telegram.org/"

# https://api.telegram.org/botTOKEN/getUpdates
# https://api.telegram.org/botTOKEN/sendMessage

# Bot api key and username
# Searches for a message from the given user and return chat_id
def get_telegram_chat_id(bot_api_key, username):
    buf = requests.post(f"{api_base_url}bot{bot_api_key}/getUpdates").json()
    for buf2 in buf['result']:
        if buf2['message']['chat']['username'] == username:
            return buf2['message']['chat']['id']

    return 'not_found'


if __name__ == '__main__':
    r = get_telegram_chat_id(sys.argv[1], sys.argv[2])
    print(r)