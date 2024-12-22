import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# Fetch the sender's IP address using a third-party API
def get_user_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")  # Fetch the IP address from ipify API
        ip = response.json().get("ip", "Unable to get IP")  # Extract the IP from the JSON response
        return ip  # Return the IP address
    except Exception as e:
        print(f"Error fetching IP: {e}")  # Handle errors during the IP fetch process
        return "Unable to get IP"  # Return a default message in case of an error

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send a welcome message when the bot is started
    await update.message.reply_text("Hello! I am active. Add me to any group!")

async def reply_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Reply with the user's IP address when a message is sent in the group
    if update.message.chat.type in ['group', 'supergroup']:  # Check if the message is from a group
        user_message = update.message.text  # Get the text of the message
        user_ip = get_user_ip()  # Fetch the user's IP address
        await update.message.reply_text(f"Hello, your IP address is {user_ip}. You said: {user_message}")  # Send the reply

def main():
    # Main function to start the bot
    BOT_TOKEN = os.getenv("BOT_TOKEN")  # Get the bot token from environment variables
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set in environment variables!")  # Ensure the bot token is available

    # Initialize the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))  # Handle the "/start" command
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_message))  # Handle text messages

    # Run the bot
    application.run_polling()  # Start the bot with polling

if __name__ == "__main__":
    main()  # Run the main function when the script is executed
