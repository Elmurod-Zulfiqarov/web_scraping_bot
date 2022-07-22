import logging

from telegram import Update, ForceReply, ReplyKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.


def start(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /start is issued."""
	user = update.effective_user
	update.message.reply_markdown_v2(
		fr'Assalomu alaykum {user.mention_markdown_v2()}\! asaxiy saytidan mahsulotlarni qidirishingiz mumkin Buni uchun bizga qidirayotgan mahsulotingiz nomini kiriting'
	)


def help_command(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /help is issued."""
	update.message.reply_text('asaxiy.uz saytidan mahsulotlarni qidirishingiz mumkin\n'
                            'Buni uchun bizga qidirayotgan mahsulotingiz nomini kiriting!')



def asaxiy_saerch(update: Update, context: CallbackContext) -> None:
	"""asaxiy.uz product search"""
	import requests
	from bs4 import BeautifulSoup

	search = update.message.text
	url = f"https://asaxiy.uz/product?key={search}"

	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")

	products = list(soup.find("div", class_="custom-gutter").find_all("div", recursive=False))[:10]
	for item in products:
		text = ""

		img = item.find("img", class_="img-fluid lazyload").get("data-src")
		if img[-5:]=='.webp':
			img = img[:-5]

		title = str(item.find("h5", class_="product__item__info-title").text)
		text += title + "\n\n" 
		
		old_price = item.find("div", class_="product__item-old--price")
		if old_price:
			old_price_text = old_price.text
			text += f"<i>{old_price_text}</i> \n\n"

		price = str(item.find("div", class_="produrct__item-prices--wrapper").text)
		text += price + "\n\n" 

		link = "https://asaxiy.uz" + str(item.find("a", class_="title__link").get("href"))
		text += link
		if img or text:
			update.message.reply_photo(img, text, parse_mode=ParseMode.HTML)
		else:
			update.message.reply_text('qayatdan urining')

def main() -> None:
	"""Start the bot."""
	# Create the Updater and pass it your bot's token.
	updater = Updater("5523799480:AAGjJg8CU57s3lQSNiwPe-ar0hAqoaPov1c")

	# Get the dispatcher to register handlers
	dispatcher = updater.dispatcher

	# on different commands - answer in Telegram
	dispatcher.add_handler(CommandHandler("start", start))
	dispatcher.add_handler(CommandHandler("help", help_command))
	dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, asaxiy_saerch))

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
	main()




