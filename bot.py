import os
import time
import telebot
from telethon import TelegramClient
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from postingformat import format_post
from command import handle_start, handle_latest, handle_buttons, check_permissions

# Load environment variables from .env
load_dotenv()

# Bot setup
BOT_TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = os.getenv('OWNER_ID')
RSS_CHANNEL_ID = os.getenv('RSS_CHANNEL_ID')
LINK_LOG_CHANNEL_ID = os.getenv('LINK_LOG_CHANNEL_ID')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL'))
WEBSITE_URL = os.getenv('WEBSITE_URL')

# API credentials for Telethon
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

# Initialize Telethon client
client = TelegramClient('bot_session', API_ID, API_HASH)
client.start()

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Function to fetch the latest magnet links
async def fetch_magnet_links():
    try:
        # Using Telethon client to scrape data from the website
        response = requests.get(WEBSITE_URL)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            posts = soup.find_all('div', {'class': 'ipsType_break ipsContained'})

            if posts:
                for post in posts:
                    title = post.find('a').text.strip()
                    link = post.find('a')['href']
                    magnet_link = get_magnet_link(link)

                    # Format the post before sending
                    formatted_post = format_post(title, magnet_link)

                    # Send the formatted post to the RSS channel
                    await client.send_message(RSS_CHANNEL_ID, formatted_post)
                    time.sleep(random.uniform(2, 4))  # Random sleep to avoid detection

                    # Send title, quality, and languages to the log channel
                    log_details = f"Title: {title}\nQuality: N/A\nLanguages: N/A"
                    await client.send_message(LINK_LOG_CHANNEL_ID, log_details)
                    time.sleep(random.uniform(2, 4))  # Random sleep to avoid detection
        else:
            print(f"Error fetching data: Status Code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching magnet links: {e}")

# Function to extract magnet link from a post
def get_magnet_link(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        magnet_link = next((a['href'] for a in soup.find_all('a', href=True) if 'magnet:' in a['href']), None)
        return magnet_link
    except Exception as e:
        print(f"Error extracting magnet link: {e}")
        return None

# Scheduler for periodic tasks
scheduler = BackgroundScheduler()

# Schedule the task to run every CHECK_INTERVAL seconds
scheduler.add_job(fetch_magnet_links, 'interval', seconds=CHECK_INTERVAL)

# Start the scheduler
scheduler.start()

# Command Handlers
@bot.message_handler(commands=['start'])
def start_command(message):
    handle_start(message)

@bot.message_handler(commands=['latest'])
def latest_command(message):
    check_permissions(message)
    handle_latest(message)

@bot.message_handler(commands=['buttons'])
def buttons_command(message):
    check_permissions(message)
    handle_buttons(message)

# Function to check user permissions (owner only)
def check_permissions(message):
    if message.from_user.id != int(OWNER_ID):
        bot.reply_to(message, "This bot is only available for the admin (owner).")
        return False
    return True

# Running the bot
if __name__ == "__main__":
    bot.polling(none_stop=True)
