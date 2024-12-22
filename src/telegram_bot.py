# Import the Update class from the telegram module
from telegram import Update

# Import necessary classes from the telegram.ext module for handling bot commands and messages
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import os

# Define the function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send a welcome message when the bot is started
    await update.message.reply_text("Hello! I am active. Add me to any group!")

# Define the function to handle the /getmyinfo command
async def get_my_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with detailed information about the user, message, and chat."""

    # Get the user who sent the message
    user = update.message.from_user

    # Get the chat where the message was sent
    chat = update.message.chat

    # Get the message details
    message = update.message

    # Check if the user has a username, otherwise assign "No username"
    username = user.username if user.username else "No username"

    # Get the text of the message, or assign "No text" if the message is empty
    message_text = message.text if message.text else "No text"

    # Collect all relevant information in a formatted string
    reply_message = (
        f"User Information:\n"
        f"ID: {user.id}\n"  # User's unique ID
        f"First Name: {user.first_name}\n"  # User's first name
        f"Last Name: {user.last_name if user.last_name else 'N/A'}\n"  # User's last name (if available)
        f"Username: @{username}\n"  # User's Telegram username
        f"Language: {user.language_code}\n\n"  # User's language code

        f"Chat Information:\n"
        f"ID: {chat.id}\n"  # Chat's unique ID
        f"Type: {chat.type}\n"  # Type of chat (private, group, supergroup, etc.)
        f"Title: {chat.title if chat.type != 'private' else 'Private chat'}\n"  # Chat title (if it's a group chat)

        f"Message Information:\n"
        f"Message ID: {message.message_id}\n"  # Unique ID of the message
        f"Text: {message_text}\n"  # The text content of the message
        f"Date: {message.date}\n\n"  # Date the message was sent

        f"Additional Information:\n"
        f"Update ID: {update.update_id}\n"  # Unique ID of the update
        f"Entities: {message.entities if message.entities else 'No entities'}\n"  # Message entities (if any)
    )

    # Reply to the user with the collected information
    await update.message.reply_text(reply_message)

# Main function to initialize and run the bot
def main():
    # Get the bot token from environment variables
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    # Check if the BOT_TOKEN is not set in the environment variables
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set in environment variables!")

    # Initialize the bot application using the provided bot token
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handler for the /start command to send a welcome message
    application.add_handler(CommandHandler("start", start))

    # Add handler for the /getmyinfo command to send detailed information
    application.add_handler(CommandHandler("getmyinfo", get_my_info))

    # Add handler for handling text messages (not commands)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_message))

    # Run the bot to listen for incoming messages and commands
    application.run_polling()

# Function to handle replies for non-command messages (e.g., when the user sends a message in a group)
async def reply_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with 'Hello' when a message is sent in the group."""
    # Check if the message was sent in a group or supergroup
    if update.message.chat.type in ['group', 'supergroup']:
        # Reply with a simple greeting
        await update.message.reply_text("Hello")

# Run the main function to start the bot when the script is executed
if __name__ == "__main__":
    main()
