# Telegram Bot Deployment on Koyeb

## Steps to Deploy on Koyeb:

### 1. Create a Koyeb account:
Go to [https://www.koyeb.com/](https://www.koyeb.com/) and sign up for a free account.

### 2. Set up Environment Variables:
Go to the Koyeb dashboard and create a new service. Under the Environment Variables section, add the following variables:
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
- `OWNER`: The admin/owner’s Telegram user ID.
- `RSS_CHANNEL_ID`: The channel ID where magnet links are posted.
- `LINK_LOG_CHANNEL_ID`: The channel ID where the movie details are logged.

### 3. Deploy Your Bot:
- Clone this repository to your local machine.
- Push the repository to Koyeb or link the GitHub repo to Koyeb directly.
- Koyeb will automatically detect the Dockerfile and deploy the bot.

### 4. Testing:
Once deployed, send the `/start` and `/latest` commands in the bot's chat to verify everything is working.

**Commands:**
- `/start`: Start the bot and get a welcome message.
- `/latest`: Fetch the latest post's magnet link from 1TamilMV and send it to the admin.

### 5. Handling Errors:
If the bot doesn't start, check the Koyeb logs for any issues with missing dependencies or environment variables.

Enjoy your bot, and happy movie posting!
