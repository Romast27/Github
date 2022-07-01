from bs4 import BeautifulSoup
import requests
import telebot
from telebot import types


TOKEN = "5301543802:AAG56VSdSm5P0EPQhqapLrlmTgfCF_Er04M"
def upcomming_spartak_match():
    with open("site.html", "r") as file:
        src = file.read()
    # url_sp = 'https://spartak.com/match'
    # req_sp = requests.get(url_sp)
    soup = BeautifulSoup(src, "lxml")
    match = soup.find_all("div", class_="_1NFj09zI active")
    res_str = str()
    tur1 = match[0]
    print(tur1.text)
    #tur = tur1.find("span", class_="_3TNvtvPF")
    for i in match:
        if i.find("div", class_="_1yJcNBpe") is None:
            teams = i.find_all("span", class_="_30dPs-1O")
            tur = tur[:-2] + str(int(tur[-2]) + 1)
            date = i.find("div", class_="_1WuJZ2Eb topLine").text
            res_str += teams[0].text + " vs " + teams[1].text + " - " + date + "\n" + tur + "\n"
    return res_str


def past_spartak_match():
    url_sp = 'https://spartak.com/match'
    req_sp = requests.get(url_sp)
    soup = BeautifulSoup(req_sp.text, "lxml")
    res_str = str()
    teams = soup.find_all("div", class_="_3Bb33bLP")
    score = soup.find_all("div", class_="Z6YDlefC")
    num_date = soup.find_all("div", class_="K5yZMJiy")
    mon_date = soup.find_all("div", class_="oH0vE5Wj")
    for i in range(0, len(teams), 2):
        res_str += f"{teams[i].text} {score[i // 2].text} {teams[i + 1].text} - {num_date[i // 2].text} " \
                   f"{mon_date[i // 2].text}\n"
    return res_str


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Привет!')

        def button_message():
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            help_item = types.KeyboardButton("Помощь")
            markup.add(help_item)
            match_item = types.KeyboardButton("Результаты Матчей")
            markup.add(match_item)
            upmatch_item = types.KeyboardButton("Будущие Матчи")
            markup.add(upmatch_item)
            bot.send_message(message.chat.id, 'Если хочешь посмотреть результаты матчей выбери "Результаты Матчей". '
                                              'Если хочешь посмотреть будущие матчи выбери "Будущие Матчи".',
                             reply_markup=markup)

        button_message()

    @bot.message_handler(content_types='text')
    def message_reply(message):
        if message.text == "Помощь":
            bot.send_message(message.chat.id, 'Привет! Если хочешь посмотреть результаты '
                                              'матчей выбери "Результаты Матчей". '
                                              'Если хочешь посмотреть будущие матчи выбери "Будущие Матчи".')
        elif message.text == "Результаты Матчей":
            bot.send_message(message.chat.id, past_spartak_match())
        elif message.text == "Будущие Матчи":
            bot.send_message(message.chat.id, upcomming_spartak_match())

    bot.infinity_polling(non_stop=True)


if __name__ == '__main__':
    upcomming_spartak_match()
    # telegram_bot(TOKEN)
