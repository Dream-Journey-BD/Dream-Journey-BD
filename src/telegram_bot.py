from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the bot is started."""
    await update.message.reply_text("Hello! I am active. Add me to any group!")

async def reply_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with detailed information about the update."""
    user = update.message.from_user
    chat = update.message.chat
    message = update.message
    username = user.username if user.username else "No username"
    message_text = message.text if message.text else "No text"

    # Collecting all relevant information
    reply_message = (
        f"User Information:\n"
        f"ID: {user.id}\n"
        f"First Name: {user.first_name}\n"
        f"Last Name: {user.last_name if user.last_name else 'N/A'}\n"
        f"Username: @{username}\n"
        f"Language: {user.language_code}\n\n"

        f"Chat Information:\n"
        f"ID: {chat.id}\n"
        f"Type: {chat.type}\n"
        f"Title: {chat.title if chat.type != 'private' else 'Private chat'}\n"

        f"Message Information:\n"
        f"Message ID: {message.message_id}\n"
        f"Text: {message_text}\n"
        f"Date: {message.date}\n\n"

        f"Additional Information:\n"
        f"Update ID: {update.update_id}\n"
        f"Entities: {message.entities if message.entities else 'No entities'}\n"
    )

    # Reply with the collected data
    await update.message.reply_text(reply_message)

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
