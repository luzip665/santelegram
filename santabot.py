#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to make a Telegram advent calendar.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
"""
import configparser
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot

try:
	import json
except ImportError:
	import simplejson as json


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__) # i.e le logger va afficher de quel fichier du package
DEBUG = True # if True, accepte des demandes à des moments random
MONTH = 12
config_file_name = "config.ini" # super original hein


## READ config file and set Auth variables
def init_api():
	config = configparser.ConfigParser()
	config.read(config_file_name)
	API_KEY = config['API']['TOKEN']
	CONVERSATIONS =  json.loads(config['API']['conversations'])
	START_TIME = int(config['CONFIG']['STARTTIME'])
	STOP_TIME = int(config['CONFIG']['STOPTIME'])
	return(API_KEY,CONVERSATIONS, START_TIME, STOP_TIME)

## SET GLOBAL VARIABLES
(API_KEY,CONVS, START_TIME, STOP_TIME) = init_api()

########### FUNCTIONS ######## 

"""Öffnen Sie die Konfigurationsdatei und lesen Sie den Tipp in der Kategorie, das ist in Ordnung
   chat_id muss eine Zeichenfolge sein
"""
def read_config(section,key):
	config=configparser.ConfigParser()
	config.read(config_file_name)
	config_value = config[section][key]
	# logger.info("read "+str(key)+" : "+config_value)
	return(config_value)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
	"""Send a message when the command /start is issued."""
	send_message(update, read_config("CONFIG", "starttext"))


# Tip abgeben
def tip(update, context):
	"""Send a random msg when the command /tip is issued."""
	logger.info("tip : "+str(update.message))
	tip = str(update.message.text)[5:]
	if(tip):
		# update.message.reply_text("Dein Tipp ist: " + tip)
		send_message(update, "Dein Tipp ist: " + tip)
		notify(tip, update, context)
	else:
		# update.message.reply_markdown_v2(read_config("CONFIG","tip"))
		send_message(update, read_config("CONFIG","tip"))

# Für den Moderator, um Tipp zu genehmigen
def approve(update,context):
	if(update.message.chat_id == int(read_config("API","PROPRIO"))):
		print(update.message.caption_markdown_v2)
		tip = update.message.text[9:]
		config2=configparser.ConfigParser()
		config2.read("submissions.ini")
		array_of_submissions = json.loads(config2["SUBMISSIONS"]["ARRAY"])
		array_of_submissions.append(tip)
		config2["SUBMISSIONS"]["ARRAY"] = json.dumps(array_of_submissions)
		with open("submissions.ini", "w") as submissionsfile:
			config2.write(submissionsfile)
		logger.info("user : "+str(update.message.from_user.first_name)+" added tip : "+tip)
		# update.message.reply_text("hinzugefügt")
		send_message(update, "hinzugefügt")


def notify(tip, update, context):
	"""Eine Nachricht an den Eigentümer mit /tip <nachricht>
		PROPRIO ist die Chat-ID vom Eigentümer
	"""
	notification = "Tip de "+str(update.message.from_user.first_name)+" (id:"+str(update.message.from_user.id)+")"
	notified_id = int(read_config("API", "PROPRIO"))
	context.bot.send_message(chat_id=notified_id, text=notification)
	message = context.bot.send_message(chat_id=notified_id, text=tip)


"""gibt den Tag zurück, wenn er im Dezember (oder im Monat MONAT) zwischen 9 und 11 Uhr liegt"""
def is_time_ok(date):
	if(date.month == MONTH or DEBUG):
		if(date.hour >= START_TIME and date.hour <= STOP_TIME or DEBUG):
			return date.day
		else:
			return False
	else:
		return False

def open_day(update,context):
	"""Sends a tip if and only if the right sender issues /open"""
	# logger.info(update)
	if(str(update.message.chat.id) in CONVS):
		chat = CONVS[str(update.message.chat.id)]
		# logger.info("chat : "+chat)
		day=is_time_ok(update.message.date)
		# logger.info("day : "+str(day))
		if(day):
			authorized_users = json.loads(read_config(chat,"users"))[day-1]
			logger.info("users : "+str(authorized_users)+" , open request from : "+str(update.message.from_user.id)+":"+update.message.from_user.first_name)
			logger.info(update.message.from_user.username)
			if(update.message.from_user.id in authorized_users):
				# update.message.reply_text(read_config("CONFIG","opentext")+" "+str(update.message.from_user.first_name))
				send_message(update, read_config("CONFIG","opentext")+" "+str(update.message.from_user.first_name))
				array = json.loads(read_config(chat,"messages")) # -1 vu que l'array, contrairement au mois, commence à zéro
				tip = array[day-1]
				logger.info(tip)
				send_message(update, tip)
			else:
				# update.message.reply_markdown_v2("Das ist nicht Dein Tag")
				send_message(update, "Das ist nicht Dein Tag")


def send_message(update, msg: str):
	if msg.strip().startswith('['):
		lines = json.loads(msg)
	else:
		lines = [msg]
	for line in lines:
		if msg.startswith('IMAGE:'):
			file = line[6:]
			photo = open(file, 'rb')
			update.message.reply_photo(photo)
		elif msg.startswith('MARKDOWN:'):
			update.message.reply_markdown_v2(line[9:])
		else:
			update.message.reply_text(line)

def help(update, context):
	"""Send a message when the command /help is issued."""
	send_message(update, read_config("CONFIG", "help"))

def erreur(update, context):
	"""Echo the user message."""
	send_message(update, read_config("CONFIG", 'error'))
	# update.message.reply_text(read_config("CONFIG",'error'))
	# logger.info("erreur : "+str(update))


def error(update, context):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
	"""Start the bot."""
	# Create the Updater and pass it your bot's token.
	# Make sure to set use_context=True to use the new context based callbacks
	# Post version 12 this will no longer be necessary
	updater = Updater(API_KEY, use_context=True)

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("tip", tip))
	dp.add_handler(CommandHandler("approve", approve))
	dp.add_handler(CommandHandler("open", open_day))

	# on noncommand i.e message - echo the message on Telegram
	dp.add_handler(MessageHandler(Filters.text, erreur))

	# log all errors
	# dp.add_error_handler(error)

	# Start the Bot
	updater.start_polling()


	# bot = Bot(API_KEY)
	# print(bot.send_message("CHAT-ID", 'Message'))

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
	main()
