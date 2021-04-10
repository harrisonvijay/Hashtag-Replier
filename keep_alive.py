# using flask to keep the bot alive
# even if replit is closed
from flask import Flask
from threading import Thread

app = Flask('')

# uptimerobot service pings this route periodically
# so that replit won't shut down the console due to inactivity
@app.route('/')
def home():
    return "Bot is running."

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()