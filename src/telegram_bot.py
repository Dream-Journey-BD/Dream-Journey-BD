import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Store chat_ids in a list (this can be replaced with a database for persistence)
chat_ids = []

async def send_workflow_start_message(application) -> None:
    """Send a 'Workflow Start' message to all groups where the bot is added."""
    for chat_id in chat_ids:
        await application.bot.send_message(chat_id, "Workflow Start")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the bot is added to a group."""
    chat_id = update.message.chat.id  # Get the chat_id dynamically
    if chat_id not in chat_ids:  # Store the chat_id to avoid duplicates
        chat_ids.append(chat_id)
    await update.message.reply_text("Hello! I am active. Add me to any group!")

async def reply_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with the sender's message text."""
    if update.message.chat.type in ['group', 'supergroup']:
        user_message = update.message.text
        await update.message.reply_text(f"Hello! You said: {user_message}")

def main():
    """Main function to start the bot."""
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set in environment variables!")

    # Initialize the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Send "Workflow Start" message when the bot starts
    application.run_async(send_workflow_start_message(application))

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_message))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
