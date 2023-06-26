import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
import re
from urllib.parse import urlparse
import requests
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # message = update.message.text
    # chat_id = update.message.chat_id
    # message_id = update.message.message_id

    # if message.startswith('BV'):
    #     new_message = message.replace('BV', 'AV')
    #     context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=new_message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="aaaa")


def find_b23_urls(content: str):
    """
    given a string possibly contains multiple urls, return the parsed url with netloc=b23.tv
    if there's no url, return empty list
    """
    list_of_url_strs = re.findall(r'(https?://\S+)', content)
    if not list_of_url_strs:
        return []
    list_of_url = [urlparse(url) for url in list_of_url_strs]
    filtered_b23_url = [url for url in list_of_url if url.netloc == 'b23.tv']
    return filtered_b23_url


def access_b23_url_and_return_real_url(url: str):
    # res = requests.get(url, allow_redirects=False)
    # real_url = res.headers['Location']
    # r = urlparse(real_url)
    # return r.scheme + "://" + r.netloc + r.path
    res = requests.get(url, allow_redirects=True)
    real_url = res.url
    r = urlparse(real_url)
    return r.scheme + "://" + r.netloc + r.path


async def remove_b23(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    filtered_b23_url = find_b23_urls(message)
    if filtered_b23_url:
        # Construct the reply message
        user_name = update.message.from_user.name
        url_list = [access_b23_url_and_return_real_url(url.geturl()) for url in filtered_b23_url]
        urls_str = "\n".join(url_list)
        content = f"{user_name} 分享了B23链接为:\n{urls_str}"
        # Send the new message
        await context.bot.send_message(chat_id=update.effective_chat.id, text=content)
        # Delete the original message
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)


async def complete_BV(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    if message.startswith("BV"):
        await update.message.reply_text(f"https://b23.tv/{message}")


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    remove_b23_handler = MessageHandler(telegram.ext.filters.Entity("url"), remove_b23)
    complete_BV_handler = MessageHandler(telegram.ext.filters.Regex(r"^BV"), complete_BV)
    start_handler = CommandHandler('start', start_handler)
    application.add_handler(start_handler)
    application.add_handler(remove_b23_handler)
    application.add_handler(complete_BV_handler)
    application.run_polling()
