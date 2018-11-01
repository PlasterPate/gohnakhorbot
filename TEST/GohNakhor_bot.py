import time
import sqlite3
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import urllib3

# proxy_url = "http://proxy.server:3128"
# telepot.api._pools = {
#    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
# }
# telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))


bot = telepot.Bot('675516835:AAFu6xoROI8wHwV7Eb5kHvBf2z8idexfWiQ')
db = sqlite3.connect("akram2.db", check_same_thread=False, timeout=10)
cursor = db.cursor()
# cursor.execute("""DROP TABLE akram_table""")
cursor.execute('''CREATE TABLE IF NOT EXISTS akram_table
               (person_id INTEGER PRIMARY KEY AUTOINCREMENT ,
                message_id INTEGER ,
                sender_id INTEGER ,
                sender_name TEXT,
                sender_username TEXT ,
                from_id INTEGER ,
                from_name TEXT,
                from_username TEXT ,
                chat_id INTEGER ,
                chat_title TEXT ,
                chat_type TEXT ,
                command TEXT)''')


def handle(msg):
    if 'message_id' in msg:
        message_id = msg['message_id']
    else:
        message_id = None
    sender_id = msg['from']['id']
    sender_name = msg['from']['first_name']
    sender_username = msg['from']['username']
    chat_id = sender_id
    if 'chat' in msg and msg['chat']['type'] == 'group':
        chat_id = msg['chat']['id']
        chat_title = msg['chat']['title']
        chat_type = msg['chat']['type']
    else:
        chat_title = None
        chat_type = None
    if 'forward_from' in msg:
        from_id = msg['forward_from']['id']
        from_name = msg['forward_from']['first_name']
        from_username = msg['forward_from']['username']
    else:
        from_id = None
        from_name = None
        from_username = None
    if 'date' in msg:
        date = msg['date']
    else:
        date = None
    if 'text' in msg:
        command = str(msg['text'])
        command_type = telepot.glance(msg)[0]
    else:
        command = None

    params = (message_id,
              sender_id, sender_name, sender_username,
              from_id, from_name, from_username,
              chat_id, chat_title, chat_type,
              command)
    cursor.execute("""insert into akram_table VALUES (null,?,?,?,?,?,?,?,?,?,?,?) """, params)
    db.commit()
    cursor.execute('''SELECT * FROM  akram_table''')
    data = cursor.fetchall()
    if telepot.flavor(msg) == 'chat':
        if command_type == 'text':
            if from_id is None:
                if command == '/start':

                    bot.sendMessage(chat_id, 'hey! \n'
                                             'forward a message from someone who you want to tell him/her Goh Nakhor!\n'
                                             'and leave the rest to me 😏')
                elif command.lower().__contains__('fuck'):
                    bot.sendMessage(chat_id, 'shut the Fuck up')
                else:
                    bot.sendMessage(chat_id, 'chi goh mikhori?')
            else:
                try:
                    bot.forwardMessage(from_id, data[len(data) - 1][2], data[len(data) - 1][1])
                    bot.sendMessage(from_id, 'Goh Nakhorrr!')
                    bot.sendMessage(sender_id, 'done!')
                except:
                    bot.sendMessage(sender_id, 'fucking failed!')
    # elif telepot.flavor(msg) == 'callback_query':
    #     query_id = telepot.glance(msg, flavor='callback_query')[0]
    #     query_data = telepot.glance(msg, flavor='callback_query')[2]
    #     bot.answerCallbackQuery(query_id, query_data + ' 😜')


# keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='siktir')],
#                                          [KeyboardButton(text='siktir2'),
#                                           KeyboardButton(text='siktir3')]])
#
# inline_keyboard = InlineKeyboardMarkup(inline_keyboard=
#                                                            [
#                                                                [InlineKeyboardButton(text='press me 🤡', callback_data='press')]
#                                                            ])
MessageLoop(bot, handle).run_as_thread()

while 1:
    time.sleep(10)
db.close()
