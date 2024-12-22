from telegram.ext import Updater, MessageHandler, Filters

# Replace 'YOUR_BOT_TOKEN' with your bot's token
BOT_TOKEN = 'YOUR_BOT_TOKEN'

# Dictionary to store group IDs
group_ids = set()

# Function to welcome the bot to new groups
def welcome_new_group(update, context):
    global group_ids
    chat_id = update.effective_chat.id  # Get the group ID
    group_ids.add(chat_id)  # Add the group ID to the set
    if update.effective_chat.type in ['group', 'supergroup']:
        context.bot.send_message(chat_id=chat_id, text="Hi! I'm your bot!")
        print(f"Bot added to group: {chat_id}")  # Log the group ID

# Function to send periodic messages
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

    # Handle when the bot is added to a new group
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome_new_group))

    # Start the bot
    updater.start_polling()

    # Periodic job setup
    job_queue = updater.job_queue
    job_queue.run_repeating(send_periodic_message, interval=300, first=10)  # Send every 5 minutes

    updater.idle()

if __name__ == "__main__":
    main()
