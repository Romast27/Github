import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types


image_k = 1
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/98.0.4758.141 YaBrowser/22.3.2.644 Yowser/2.5 Safari/537.36"
}


def save_data(name, file_data):
    file = open(name, 'bw')
    for chunk in file_data.iter_content(4096):
        file.write(chunk)


def get_name(url):
    name = url.split('/')[-1]
    return name


def get_image(url):
    global image_k
    file_d = requests.get(url, stream=True)
    name = "image" + str(image_k)
    save_data(name, file_d)
    image_k += 1


def colon_of_news():
    url_news = "https://www.hltv.org/"
    r_news = requests.get(url_news, headers=headers)
    soup_news = BeautifulSoup(r_news.text, "lxml")
    news = soup_news.find("div", class_="standard-box standard-list").find_all(class_="newstext")
    return_str = str()
    for new in news:
        return_str += new.text + '\n'
    return return_str


def result_matches():
    try:
        url_matches = "https://www.hltv.org/results"
        r_matches = requests.get(url_matches, headers=headers)
        soup_result = BeautifulSoup(r_matches.text, "lxml")
        resmatches = soup_result.find("div", "big-results")
        teams = resmatches.find_all("div", class_="team")
        score = resmatches.find_all("td", class_="result-score")
        event = resmatches.find_all("td", class_="event")
        return_str = str()
        for i in range(len(event)):
            return_str += f'{teams[i * 2].text} vs {teams[i * 2 + 1].text} - {event[i].text} \n' \
                          f'Score: {score[i].text}\n\n'
        return return_str
    except AttributeError:
        return "There isn't any current matches"


def current_matches():
    try:
        url_matches = "https://www.hltv.org/matches"
        r_matches = requests.get(url_matches, headers=headers)
        soup_matches = BeautifulSoup(r_matches.text, "lxml")
        livematches = soup_matches.find("div", class_="liveMatches")
        matches = livematches.find_all(class_="matchTeamName text-ellipsis")
        event = livematches.find(class_="matchEventName gtSmartphone-only")
        maps = livematches.find_all("div", "liveMatch-container")
        img_logo = soup_matches.find("div", "liveMatchesContainer").find_all("div", "matchTeamLogoContainer")
        return_str = str()
        for item in img_logo:
            if "teamlogo" in item.find("img")["src"]:
                get_image(item.find("img")["src"])
        for i in range(len(maps)):
            try:
                if int(maps[i]["stars"]) > 0:
                    return_str += f'{matches[i * 2].text} vs {matches[i * 2 + 1].text}' \
                                  f' - {event.text}\nMaps: {maps[i]["data-maps"]}\n\n'
            except AttributeError:
                continue
        if return_str != '':
            return return_str
        else:
            return "There isn't any current matches"
    except AttributeError:
        return "There isn't any current matches"


def upcoming_matches():
    try:
        url_matches = "https://www.hltv.org/matches"
        r_matches = requests.get(url_matches, headers=headers)
        soup_matches = BeautifulSoup(r_matches.text, "lxml")
        upcomingmatches = soup_matches.find("div", class_="upcomingMatchesSection")
        date = upcomingmatches.find("span")
        first_team = upcomingmatches.find_all("div", class_="matchTeam team1")
        second_team = upcomingmatches.find_all("div", class_="matchTeam team2")
        event = upcomingmatches.find(class_="matchEventName gtSmartphone-only")
        star = soup_matches.find_all("div", class_="upcomingMatch")
        time = upcomingmatches.find_all(class_="matchTime")
        return_str = date.text + '\n\n'
        for i in range(len(first_team)):
            if int(star[i]["stars"]) > 0:
                return_str += "{} vs {} - {}\nTime: {}".format(first_team[i].text.replace('\n', ''),
                                                               second_team[i].text.replace('\n', ''), event.text,
                                                               time[i].text) + '\n\n'
        return return_str
    except AttributeError:
        return "There isn't any upcoming matches"


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Hello!')

        def button_message(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            help_item = types.KeyboardButton("Help")
            news_item = types.KeyboardButton("News")
            match_item = types.KeyboardButton("Current Matches")
            upmatch_item = types.KeyboardButton("Upcomming Matches")
            result_item = types.KeyboardButton("Result Matches")
            markup.add(help_item, news_item, match_item, upmatch_item, result_item)
            bot.send_message(message.chat.id, 'If you want to check nearest news chose "News". '
                                              'If you want to check current matches write "Current Matches". '
                                              'If you want to check upcoming matches write "Upcomming Matches".'
                                              'If you want to check upcoming matches write "Result Matches".',
                             reply_markup=markup)
        button_message(message)

    @bot.message_handler(content_types='text')
    def message_reply(message):
        if message.text == "Help":
            bot.send_message(message.chat.id, 'Hello! If you want to check nearest news chose "News". '
                                              'If you want to check current matches write "Current Matches". '
                                              'If you want to check upcoming matches write "Upcomming Matches".'
                                              'If you want to check upcoming matches write "Result Matches".')
        elif message.text == "News":
            bot.send_message(message.chat.id, colon_of_news())
        elif message.text == "Current Matches":
            bot.send_message(message.chat.id, current_matches())
        elif message.text == "Upcomming Matches":
            bot.send_message(message.chat.id, upcoming_matches())
        elif message.text == "Result Matches":
            bot.send_message(message.chat.id, result_matches())

    bot.polling(none_stop=True)


if __name__ == '__main__':
    with open("site.html", "w") as file:
        response = requests.get(url="https://spartak.com/match")
        file.write(response.text)
    telegram_bot(TOKEN)
