import asyncio
import logging
import os
from flask import Flask
import threading
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    error,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.ERROR
)
logger = logging.getLogger(__name__)

# Token del bot
BOT_TOKEN = "7532080955:AAHJZnI4B23a2vvzKQJawAAPIvYNdtSIUqs"

# Link Web App
WEBAPP_LINK = "https://ryo88creator.github.io/seriebot/"

# Canali obbligatori
REQUIRED_CHANNELS = ["@NostraReteCanali", "@amznoes"]

# Funzione START
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_id = update.effective_chat.id

    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user.id)
            if member.status not in ["member", "administrator", "creator"]:
                await update.message.reply_text(
                    f"🔒 Per accedere al catalogo devi iscriverti ai canali:\n\n"
                    f"👉 {REQUIRED_CHANNELS[0]}\n"
                    f"👉 {REQUIRED_CHANNELS[1]}"
                )
                return
        except error.TelegramError:
            await update.message.reply_text("Errore durante la verifica dell'iscrizione.")
            return

    # Se iscritto
    keyboard = [
        [InlineKeyboardButton("🎬 Apri Catalogo Video", url=WEBAPP_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("✅ Accesso autorizzato!", reply_markup=reply_markup)

# Flask per mantenere vivo il bot
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot attivo!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# Avvio bot
if __name__ == '__main__':
    keep_alive()
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()
