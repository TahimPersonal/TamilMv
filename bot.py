import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OWNER = os.getenv('OWNER')
RSS_CHANNEL_ID = os.getenv('RSS_CHANNEL_ID')
LINK_LOG_CHANNEL_ID = os.getenv('LINK_LOG_CHANNEL_ID')

# Create the bot instance
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Function to fetch the latest post
def get_latest_post():
    main_url = 'https://www.1tamilmv.pm/'  # Updated website URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }

    try:
        web = requests.get(main_url, headers=headers)
        soup = BeautifulSoup(web.text, 'lxml')

        # Get the first post (latest)
        latest_post = soup.find_all('div', {'class': 'ipsType_break ipsContained'})[0]
        title = latest_post.findAll('a')[0].text.strip()
        link = latest_post.find('a')['href']
        magnet_links = get_magnet_links(link)

        if magnet_links:
            # Construct the formatted message
            message = f"/qbleech1 {magnet_links[0]}\nTag: @Mr_official_300 2142536515"
            return message
        else:
            return "No magnet link found for the latest post."

    except Exception as e:
        print(f"Error fetching latest post: {e}")
        return "Error fetching the latest post."

# Function to extract magnet links from the post
def get_magnet_links(post_url):
    try:
        html = requests.get(post_url)
        soup = BeautifulSoup(html.text, 'lxml')
        magnet_links = [a['href'] for a in soup.find_all('a', href=True) if 'magnet:' in a['href']]
        return magnet_links
    except Exception as e:
        print(f"Error retrieving magnet links: {e}")
        return []

# Command handler for /start command
def start(update, context):
    user_id = update.message.from_user.id
    if user_id == int(OWNER):
        welcome_message = "Hello 👋! This bot fetches magnet links and posts them to your channels.\n\nUse /latest to get the latest post's magnet link."
        update.message.reply_text(welcome_message)
    else:
        update.message.reply_text("This bot is only available for the admin (CPFlix).")

# Command handler for /latest command
def latest(update, context):
    user_id = update.message.from_user.id
    if user_id == int(OWNER):
        latest_post_message = get_latest_post()
        update.message.reply_text(latest_post_message)
    else:
        update.message.reply_text("This bot is only available for the admin (CPFlix).")

# Set up the Updater and Dispatcher
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("latest", latest))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
