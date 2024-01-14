import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import datetime as dt


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.")

async def get_metogram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dt_now:dt.datetime = dt.datetime.now()
    meteo_url_base:str = "https://www.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=406&col=250&lang=pl"
    if dt_now.hour < 12:
        meteo_url_suffix:str = f"{dt_now.strftime('%Y%m%d')}00"
    else:
        meteo_url_suffix:str = f"{dt_now.strftime('%Y%m%d')}12"
    meteo_url:str = f"{meteo_url_base}&fdate={meteo_url_suffix}"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=ParseMode.MARKDOWN_V2,
        text=f"*Prognoza pogody na następne 60 godzin*\nWarszawa")

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=meteo_url,
        caption=f"meteogram: {meteo_url_suffix}")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"*CAPSed* {text_caps}", parse_mode=ParseMode.MARKDOWN_V2)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="No sory, I didn't understand that command.")


if __name__ == '__main__':
    #telegram tokens
    sarmacka_chat_id:int = os.environ.get('SARMACKA_CHAT_ID') or exit(1)
    ludw_ai_chat_id:int = os.environ.get('LUDW_AI_CHAT_ID') or exit(1)
    ludwik_grazyna_chat_id:int = os.environ.get('LUDWIK_GRAZYNA_CHAT_ID') or exit(1)
    lg_bot:str = os.environ.get('TELEGRAM_LG_TOKEN') or exit(1)
    ha_bot:str = os.environ.get('TELEGRAM_HA_TOKEN') or exit(1)

    application = ApplicationBuilder().token(lg_bot).build()
    
    
    # application.add_handler(
    #     CommandHandler(['m', 'meteo'], get_metogram, filters.Chat(chat_id=ludwik_grazyna_chat_id))
    # ) 

    application.job_queue.run_once(

    # caps_handler  = CommandHandler('caps', caps, filters.Chat(chat_id=ludwik_grazyna_chat_id))
    # echo_handler  = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    # unknown_handler = MessageHandler(filters.COMMAND, unknown)

    # application.add_handler(caps_handler)
    # application.add_handler(echo_handler)
    # application.add_handler(unknown_handler)
    
    application.run_polling()