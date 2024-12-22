import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

# Fetch the token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Dictionary to store group IDs
group_ids = set()


async def welcome_new_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the bot being added to a new group and sends a welcome message.
    """
    global group_ids
    chat_id = update.effective_chat.id
    group_ids.add(chat_id)
    if update.effective_chat.type in ['group', 'supergroup']:
        await context.bot.send_message(chat_id=chat_id, text="Hi! I'm your bot!")
        print(f"Bot added to group: {chat_id}")


async def send_periodic_message(context: ContextTypes.DEFAULT_TYPE):
    """
    Periodically sends a message to all groups the bot is part of.
    """
    global group_ids
    for chat_id in group_ids:
        try:
            await context.bot.send_message(chat_id=chat_id, text="Hi! This is a periodic message.")
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")


def main():
    """
    Main function to set up and run the bot.
    """
    if not BOT_TOKEN:
        raise ValueError("Bot token not set. Ensure BOT_TOKEN is configured as an environment variable.")

    # Build the application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handler for detecting when the bot is added to a group
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_group))

    # Start periodic messages
    job_queue = application.job_queue
    job_queue.run_repeating(send_periodic_message, interval=300, first=10)  # Every 5 minutes (300 seconds)

    # Run the bot
    application.run_polling()


if __name__ == "__main__":
    main()
