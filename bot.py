import telebot
import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=["start"])
def time_sort(message):
    db_worker = SQLighter(config.database_name)
    row = db_worker.select_single()

if __name__ == '__main__':
    bot.infinity_polling()