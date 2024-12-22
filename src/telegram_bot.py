from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the bot is started."""
    await update.message.reply_text("Hello! I am active. Add me to any group!")

async def reply_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with 'Hello' followed by the user's username when a message is sent in the group."""
    if update.message.chat.type in ['group', 'supergroup']:
        username = update.message.from_user.username
        if username:  # Check if the user has a username
            await update.message.reply_text(f"Hello @{username}")
        else:
            await update.message.reply_text("Hello! User has no username.")

def main():
    """Main function to start the bot."""
    # Get the bot token from environment variables
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set in environment variables!")

    # Initialize the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_message))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
