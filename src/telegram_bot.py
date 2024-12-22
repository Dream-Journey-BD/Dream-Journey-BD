import os
from telegram.ext import Updater, MessageHandler, Filters

# Fetch the token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Dictionary to store group IDs
group_ids = set()

def welcome_new_group(update, context):
    global group_ids
    chat_id = update.effective_chat.id
    group_ids.add(chat_id)
    if update.effective_chat.type in ['group', 'supergroup']:
        context.bot.send_message(chat_id=chat_id, text="Hi! I'm your bot!")
        print(f"Bot added to group: {chat_id}")

def send_periodic_message(context):
    global group_ids
    for chat_id in group_ids:
        try:
            context.bot.send_message(chat_id=chat_id, text="Hi! This is a periodic message.")
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome_new_group))

    updater.start_polling()

    job_queue = updater.job_queue
    job_queue.run_repeating(send_periodic_message, interval=300, first=10)

    updater.idle()

if __name__ == "__main__":
    if not BOT_TOKEN:
        raise ValueError("Bot token not set. Ensure BOT_TOKEN is configured as an environment variable.")
    main()
