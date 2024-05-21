import logging
from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import requests
from telegram.ext import CallbackContext
from telegram.ext import Updater

from flask import Flask
from bs4 import BeautifulSoup
import os
from telegram import Bot
TOKEN = '5428248997:AAGzW8Av6Xj6xSRP7anhfsOuldR-YMuuaJ0'

bot = Bot(token=TOKEN)
R = " site: sci-hub "
L = " +pdf "
dispatcher = Dispatcher(bot, None, use_context=True)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Your Telegram bot token

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bot is running! Use /search <keyword> to search for PDF or DOCX files.")

def search_and_download(update: Update, context: CallbackContext):
    query = ' '.join(context.args)
    Q = query + ' ' + L
    if not query:
        update.message.reply_text("يرجى تقديم مصطلح البحث باستخدام : عنوان او مفردات البحث search / ")
        return

    search_url = f"https://www.google.com/search?q={Q} filetype:pdf OR filetype:docx"
    logger.info(f"Searching for: {search_url}")

    try:
        response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        update.message.reply_text("Failed to perform search.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    found_files = False
    for link in links:
        href = link.get('href')
        if href and ('.pdf' in href or '.docx' in href):
            if '/url?q=' in href:
                file_url = href.split('/url?q=')[1].split('&')[0]
            else:
                file_url = href

            file_name = file_url.split('/')[-1]
            file_path = os.path.join('downloads', file_name)
            logger.info(f"Found file: {file_url}")

            try:
                file_response = requests.get(file_url, headers={'User-Agent': 'Mozilla/5.0'})
                file_response.raise_for_status()
                with open(file_path, 'wb') as file:
                    file.write(file_response.content)
                update.message.reply_document(document=open(file_path, 'rb'))
                os.remove(file_path)
                logger.info(f"Downloaded and sent file: {file_path}")
                found_files = True
            except Exception as e:
                logger.error(f"Error downloading file: {e}")
                update.message.reply_text(f"يرجى الانتظار...")

    if not found_files:
        update.message.reply_text("No files found.")

def find_free_files(update: Update, context: CallbackContext):
    query = ' '.join(context.args)
    Q = query + ' ' + R
    if not query:
        update.message.reply_text("يرجى تقديم مصطلح البحث باستخدام : عنوان او مفردات البحث findfree / ")
        return

    search_url = f"https://www.google.com/search?q={Q} filetype:pdf OR filetype:docx"
    logger.info(f"Searching for free files: {search_url}")

    try:
        response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        update.message.reply_text("Failed to perform search.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    found_files = False
    for link in links:
        href = link.get('href')
        if href and ('.pdf' in href or '.docx' in href):
            if '/url?q=' in href:
                file_url = href.split('/url?q=')[1].split('&')[0]
            else:
                file_url = href

            file_name = file_url.split('/')[-1]
            file_path = os.path.join('downloads', file_name)
            logger.info(f"Found file: {file_url}")

            try:
                file_response = requests.get(file_url, headers={'User-Agent': 'Mozilla/5.0'})
                file_response.raise_for_status()
                with open(file_path, 'wb') as file:
                    file.write(file_response.content)
                update.message.reply_document(document=open(file_path, 'rb'))
                os.remove(file_path)
                logger.info(f"Downloaded and sent file: {file_path}")
                found_files = True
            except Exception as e:
                logger.error(f"Error downloading file: {e}")
                update.message.reply_text(f"يرجى الانتظار...")

    if not found_files:
        update.message.reply_text("No files found.")

def All(update: Update, context: CallbackContext):
    query = ' '.join(context.args)
    Q = query + L

    if not query:
        update.message.reply_text("Please provide a search term using: 'search / [your query]'")
        return

    search_engines = [
        "site: Lib Guides Community",
        "site: SweetSearch",
        "site: Library of Congress",
        "site: Infotopia",
        "site: Eric",
        "site: CiteuLike",
        "site: core.ac.uk",
        "site: archives.gov",
        "site: loc.gov",
        "site: sci-hub",
        "site: semanticscholar.org"
    ]

    for search_engine in search_engines:
        combined_query = f"{Q} {search_engine}"
        logger.info(f"Searching with combined query: {combined_query}")

        search_url = f"https://www.google.com/search?q={combined_query} filetype:pdf OR filetype:docx"

        try:
            response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            update.message.reply_text("Failed to perform search.")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')

        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        found_files = False
        for link in links:
            href = link.get('href')

            if href and ('.pdf' in href or '.docx' in href):
                if '/url?q=' in href:
                    file_url = href.split('/url?q=')[1].split('&')[0]
                else:
                    file_url = href

                file_name = file_url.split('/')[-1]
                file_path = os.path.join('downloads', file_name)
                logger.info(f"Found potential file: {file_url}")

                try:
                    file_response = requests.get(file_url, headers={'User-Agent': 'Mozilla/5.0'})
                    file_response.raise_for_status()

                    with open(file_path, 'wb') as file:
                        file.write(file_response.content)

                    update.message.reply_document(document=open(file_path, 'rb'))
                    os.remove(file_path)
                    logger.info(f"Downloaded and sent file: {file_path}")
                    found_files = True
                    break

                except Exception as e:
                    logger.error(f"Error downloading file: {e}")
                    update.message.reply_text(f"يرجى الانتظار ....")

        if not found_files:
            update.message.reply_text("No files found.")

def stop_search(update: Update, context: CallbackContext):
    update.message.reply_text("Search stopped.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search", search_and_download))
    dp.add_handler(CommandHandler("findfree", find_free_files))
    dp.add_handler(CommandHandler("All", All))
    dp.add_handler(CommandHandler('stop', stop_search))

    updater.start_polling()
    logger.info("Bot started successfully")
    updater.idle()


if __name__ == '__main__':
    main()
