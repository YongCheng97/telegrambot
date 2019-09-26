import json 
import requests
import time
import urllib
import telegram
import pytz
import gspread
import quickstart as qs

TOKEN = "882567029:AAHiVaS_Th6XtfKR1Czg5y6eg7tsqy433ow"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        message = update["message"]
        chat = update["message"]["chat"]["id"]
        items = ["Clock in", "Clock out"]
        if text == "/start": 
            send_message("Welcome to learnseeker! Please type /command to clock-in or clock-out", chat)
        elif text == "/command":
            keyboard = build_keyboard(items)
            send_message("Please choose an option", chat, keyboard)
        elif text == "Clock in":
            f = open("userName.txt", "w")
            f.write(str(message["from"]["first_name"].encode("utf-8")))
            f.close()
            f = open("clock.txt", "w")
            f.write("Clock-in")
            f.close()
            qs.main()
            send_message("Have a good day at work!", chat)
        elif text == "Clock out": 
            f = open("userName.txt", "w")
            f.write(str(message["from"]["first_name"].encode("utf-8")))
            f.close()
            f = open("clock.txt", "w")
            f.write("Clock-out")
            f.close()
            send_message("If you wish to input the work you have done today, please type / followed by the work you completed today! If not, you can just type /  E.g. '/ I coded an application today' ", chat) 
        elif text[0:1] == "/":
            f = open("activities.txt", "w")
            f.write(text[2:1000])
            f.close()
            qs.main()
            send_message("Goodbye!", chat)
        else:
            send_message("Incorrect message! Please try again.", chat)
    

def arr():
    from datetime import datetime, timedelta
    #date = str(datetime.now().date())
    #time = (datetime.now() + timedelta(hours=8)).time().strftime('%H:%M:%S')
    tz = pytz.timezone('Asia/Singapore')
    date = str(datetime.now(tz).date())
    time = str(datetime.now(tz).time())
    
    f = open("userName.txt", "r")
    name = f.read()
    f= open("clock.txt", "r")
    clock = f.read()
    f = open("activities.txt", "r")
    activities = f.read()
    if clock == "Clock-in":
        return [name, date, "Clock-in", time]
    elif clock == "Clock-out": 
        return [name, date, "Clock-out", time, activities]

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)    

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if "result" in updates and len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()