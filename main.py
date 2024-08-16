from fastapi import FastAPI
import requests
import json
import time
from threading import Thread

users = {}

# Define the webhook URL
webhook_url = 'https://discord.com/api/webhooks/1274065046246260856/9L3xKNQRnP8ddzN7ww7P6Xd2T9dQXJFggcqrjyYZr6wHO2bquGoHMmTaRQEw4Z-GtENS'

def rc():
    while True:
        timestamp = time.time()
        text = ""
        for user in users:
            if timestamp-users[user]>60:
                text = f'{text}:red_circle: {user}\n'
            else:
                text = f'{text}:green_circle: {user}\n'
        print(text)
        embed_data = {
            "embeds": [
                {
                    "title": 'Accounts',
                    "description": text,
                    "color": 65280
                }
            ]
        }

        # Send the POST request
        response = requests.post(
            webhook_url,
            json=embed_data,
            headers={'Content-Type': 'application/json'}
        )
        time.sleep(300)

def start_bgt():
    thred = Thread(target=rc)
    thred.daemon = True
    thred.start()


app = FastAPI()

@app.on_event("startup")
def on_startup():
    start_bgt()

@app.get('/api')
def home():
    return users

@app.get("/api/{name}/{time}")
def read_item(name: str, time: int):
    users[name] = time

import uvicorn
uvicorn.run()