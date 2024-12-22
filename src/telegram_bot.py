from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the bot is started."""
    await update.message.reply_text("Hello! I am active. Add me to any group!")

async def reply_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with detailed formatted info when a message is sent in the group."""
    if update.message.chat.type in ['group', 'supergroup']:
        user = update.message.from_user
        chat = update.message.chat
        text = update.message.text
        username = user.username if user.username else "No username"

        # Escape special characters for MarkdownV2
        response_text = (
            f"**User Info:**\n"
            f"🔹 **Name**: {user.first_name} {user.last_name}\n"
            f"🔹 **Username**: @{username}\n"
            f"🔹 **User ID**: `{user.id}`\n"
            f"🔹 **Language**: `{user.language_code}`\n\n"

            f"**Chat Info:**\n"
            f"🔹 **Chat ID**: `{chat.id}`\n"
            f"🔹 **Chat Type**: `{chat.type}`\n"
            f"🔹 **Chat Title**: `{chat.title if chat.type != 'private' else 'Private Chat'}`\n\n"

            f"**Message Info:**\n"
            f"🔹 **Message ID**: `{update.message.message_id}`\n"
            f"🔹 **Message Text**: *{text}*\n"
            f"🔹 **Date**: `{update.message.date}`\n\n"

            f"**Bot Info:**\n"
            f"🔹 **Bot Name**: [@{context.bot.username}](https://t.me/{context.bot.username})\n"
            f"🔹 **Bot ID**: `{context.bot.id}`\n\n"

            f"**Additional Info:**\n"
            f"🔹 **Update ID**: `{update.update_id}`\n"
            f"🔹 **Is Group**: `True` if the message is from a group, `False` otherwise.\n"
        )

        # Escape special characters in response text for MarkdownV2
        response_text = response_text.replace("|", "\\|")

        # Send formatted response
        await update.message.reply_text(response_text, parse_mode="MarkdownV2")

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
