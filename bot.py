import json
import datetime

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


# Define a `/start` command handler.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    await update.message.reply_text(
        "Please press the button below to see the price of $NOT.",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Live $NOT Price Display",
                web_app=WebAppInfo(url="https://notcoin-price.onrender.com/"),
            ),
            resize_keyboard=True
        ),
    )


async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = json.loads(update.effective_message.web_app_data.data)
    await update.message.reply_html(
        text=f"The price of $NOT at <b>{str(datetime.datetime.now())}</b>:\n<b>{data.get('price', '')}</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


def main() -> None:
    application = Application.builder().token("1751793994:AAHSPVz7P6THh5Admceg2wTPKXmVGkvkWlI").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
