from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import os
import requests

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the bot is started."""
    await update.message.reply_text("Hello! I am active. Add me to any group!")

async def reply_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with 'Hello' followed by the user's text when a message is sent in the group."""
    if update.message.chat.type in ['group', 'supergroup']:
        user_message = update.message.text
        await update.message.reply_text(f"Hello {user_message}")

def send_welcome_message_to_group(bot_token: str, chat_id: str) -> None:
    """Send a message to a group when the bot is started."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": "Hello! The bot is now running and active!"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Message sent to group successfully!")
    else:
        print(f"Failed to send message: {response.status_code}")

def main():
    """Main function to start the bot."""
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")  # The ID of the group you want to send a message to

    if not BOT_TOKEN or not GROUP_CHAT_ID:
        raise ValueError("BOT_TOKEN or GROUP_CHAT_ID is not set in environment variables!")

    # Send a message to the group when the bot starts
    send_welcome_message_to_group(BOT_TOKEN, GROUP_CHAT_ID)

    # Initialize the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_message))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
