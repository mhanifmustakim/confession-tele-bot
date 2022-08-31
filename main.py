from time import sleep
from secrets import (API_TOKEN, Channel_ID)  # secret environment variables
import pygsheets
import telebot

# Handle GSheets from GForm
# This requires a client_secret.json (for info read pygsheets documentation)
gc = pygsheets.authorize()

# open Google Sheets with title :
sh = gc.open('Confession Test v3.0 (Responses)')
# access the worksheet of title :
wks = sh.worksheet_by_title("Form Responses 1")

# Handle TelegramBotAPI
# GET API_TOKEN from BotFather in Telegram
bot = telebot.TeleBot(API_TOKEN)

print("Starting Bot Features")

# The first column in the gsheets
INIT_MESSAGE = "Confess anything :)"
# ChannelID of confession Channel in String format
CHANNEL_ID = Channel_ID
# Time interval to check for responses in gsheets
MIN_INTERVAL = 1

# waits for start command in the bot registered by typing "/start"
# WARNING! Anyone can call the command if they know your bot


@bot.message_handler(commands=['start'], chat_types=['private'])
def start_bot(message):
    bot.send_message(
        message.chat.id, f"Starting sync from GSheets to Channel : {CHANNEL_ID}")  # message sent to the person calling the command
    # saves lastRow read by the program (set initial value of -1)
    fh = open("lastRow.txt", "r")
    # store last row that has been sent to the channel
    lastRow = int(fh.readline())
    fh.close()
    while True:
        for i, row in enumerate(wks):
            # skip first header
            if row[1] == INIT_MESSAGE:
                continue
            # check if there is content and if the message hass already been uploaded
            elif (row[1] and i > lastRow):
                bot.send_message(CHANNEL_ID, row[1])
                lastRow = i
                fh = open("lastRow.txt", "w")
                fh.write(str(lastRow))
                fh.close()
                # sleep for 1 second to avoid overloading telegram API
                sleep(1)
        sleep(MIN_INTERVAL * 60)


bot.infinity_polling()
