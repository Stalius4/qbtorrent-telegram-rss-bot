from qbittorrent import qbt_login, qbt_functions
import asyncio
from RSS_feed import rss_feed

import os
from dotenv import load_dotenv, dotenv_values

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes,JobQueue

 
async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""

    #last_documentary() returns title, image, torrent_link, website_link, id
    new_feed = rss_feed.last_documentary()
    photo= new_feed["image"]
    message = (
        f"{new_feed['title']}\n"
        # f"Torrent link: {new_feed['torrent_link']}"
    )
    torrent_link = new_feed["torrent_link"]
    button =[[InlineKeyboardButton("Download",callback_data="torrent_link")]]
    reply_markup = InlineKeyboardMarkup(button)
    await context.bot.send_photo(chat_id=-1002283195431, photo=photo, caption= message, show_caption_above_media=True,reply_markup=reply_markup)
    context.bot_data["latest_torrent"] = torrent_link


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
   
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    qbt_client = context.bot_data["qbt_client"]
    torrent_link = context.bot_data.get("latest_torrent")
    doc = rss_feed.last_documentary() 
    if query.data == "documentary":
        await query.edit_message_text(text=(
                        f"Title: {doc.get('title', 'N/A')}\n"
                        f"Description: {doc.get('image', 'N/A')}\n"
                        f"Date: {doc.get('website_link', 'N/A')}"
        ))
    if query.data =="torrent_link":
        qbt_functions.add_torrent(qbt_client, torrent_link)
        await query.edit_message_caption(caption=f"Title: {rss_feed.last_documentary().get('title', 'N/A')}\n"
                    f"🔗 [Torrent Link]({torrent_link})",parse_mode="Markdown")
       
    else:
        await query.edit_message_text(text="another text")




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



async def list_3_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Documentary", callback_data="documentary"),
            InlineKeyboardButton("Stand-up", callback_data="stand-up"),
        ],
        [InlineKeyboardButton("Comedy", callback_data="comedy")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)







def main():
    logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)




    load_dotenv()

    # rss_feed.display_rss()
    # asyncio.run(rss_feed.async_last_documentary())
    qbt_client =qbt_login.qbt_log_in()
    # Check if login is successful 
    if qbt_client is None:
        print("Login failed; stopping execution.")
        return
    
  
  
    application = Application.builder().token(os.getenv("TOKEN")).build()
    application.bot_data["qbt_client"] = qbt_client

    list_3_buttons_handler = CommandHandler('list',list_3_buttons)
    application.add_handler(list_3_buttons_handler)
    application.add_handler(CallbackQueryHandler(button))
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    status_handler = CommandHandler("status", status)
    application.add_handler(status_handler)
    list_torrents_handler = CommandHandler("list_all", list_torrents)
    application.add_handler(list_torrents_handler)

    job_queue = application.job_queue
    if job_queue is None:
        job_queue = JobQueue()
        job_queue.set_application(application)
        job_queue.start()
    application.job_queue.run_repeating(
        alarm,
        interval=5,       # check every 60 seconds; adjust as needed
        first=0,           # start immediately
        data={"chat_id":-1002283195431} # pass the fixed chat ID
    )

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