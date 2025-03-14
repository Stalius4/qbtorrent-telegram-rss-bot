from qbittorrent import qbt_login, qbt_functions
import asyncio
from RSS_feed import rss_feed

import os
from dotenv import load_dotenv, dotenv_values

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

 



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    qbt_client = context.bot_data["qbt_client"]
    if qbt_client.auth.is_logged_in:
        result = "Qbittorrent is online"
    else:
        result = "Qbittorrent is offline"
    await context.bot.send_message(chat_id=update.effective_chat.id, text= result)



async def list_torrents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    qbt_client = context.bot_data["qbt_client"]
    result = await qbt_functions.async_list_all_torrents(qbt_client)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=result)

def main():
    load_dotenv()
    print(os.getenv("TOKEN"))
    # asyncio.run(rss_feed.async_last_documentary())
    qbt_client =qbt_login.qbt_log_in()
    # Check if login is successful 
    if qbt_client is None:
        print("Login failed; stopping execution.")
        return
    
  
  
    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()
    application.bot_data["qbt_client"] = qbt_client


    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    status_handler = CommandHandler("status", status)
    application.add_handler(status_handler)
    list_torrents_handler = CommandHandler("list_all", list_torrents)
    application.add_handler(list_torrents_handler)
    application.run_polling()
    #asyncio.run(qbt_functions.async_add_torrent(qbt_client))
    # asyncio.run(qbt_functions.async_torrent_count(qbt_client))
    # asyncio.run(qbt_functions.async_list_all_torrents(qbt_client))
if __name__ == '__main__':
    main()

#Button to add the torrent is working, but in need to be adjusted to rss feed 
#rss feed is sending last updated movie. In there should be link for torrent.
# torrent_link = rss_function()     returns last updated movie link
# asyncio.run(qbt_functions.async_add_torrent(qbt_client, torrent_link))