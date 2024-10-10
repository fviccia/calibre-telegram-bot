import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import filters
from telegram.ext import MessageHandler
from calibre import add_ebook_to_calibre

# Telegram bot token
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CALIBRE_ADRESS = os.getenv("CALIBRE_ADRESS")
CALIBRE_USER = os.getenv("CALIBRE_USER")
CALIBRE_PWD = os.getenv("CALIBRE_PWD")


# Directory to save forwarded messages
SAVE_DIR = "calibre-bot-temp-files"
os.makedirs(SAVE_DIR, exist_ok=True)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("httpx")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Send a book to save it to Calibre Library",
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.api_kwargs["forward_date"] is not None:
            if update.message.document:
                # Handle forwarded document
                document = update.message.document
                file = await context.bot.get_file(document.file_id)
                save_path = os.path.join(SAVE_DIR, document.file_name)
                # Save book
                await file.download_to_drive(save_path)

                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Forwarded document '{document.file_name}' saved locally.",
                )
                # Upload book to calibre
                try:
                    save_book = add_ebook_to_calibre(
                        save_path, CALIBRE_ADRESS, CALIBRE_USER, CALIBRE_PWD
                    )
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"{save_book}",
                    )
                    # Delete file after upload
                    os.remove(save_path)
                except Exception as e:
                    logger.error(e)

            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Forwarded message is not a document.",
                )
    except:
        # Handle regular non-forwarded messages
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="The bot for now, only accepts forwarded messages.",
        )


if __name__ == "__main__":
    if TOKEN is None:
        raise ValueError("Token cannot be None.")
    else:
        application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", start)

    application.add_handler(start_handler)

    echo_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND) | filters.Document.ALL, echo
    )
    application.add_handler(echo_handler)

    application.run_polling()
