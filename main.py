import requests
import telebot
from time import sleep
from bs4 import BeautifulSoup as b

game_list = set()
dict_for_1st_strategy = dict()
dict_for_2nd_strategy = dict()
dict_for_3rd_strategy = dict()
tgBot = telebot.TeleBot('5061487172:AAFgTi1TN_WfNAJu3jQyb666MWosv6JJpms')


# def find_matches():
#     online_games_list = ['https://soccer365.ru' + link.find('a').get('href') for link in
#                          b(requests.get('https://soccer365.ru/online/&tab=1').text, 'lxml').find_all('div',
#                                                                                                      class_='game_block online')]
#     print(online_games_list)
#     return online_games_list

def get_info_from_game(game_link):
    global event_goal_left, time, koeffright, event_goal_right, all_mins, koeffleft

    koeffleft, koeffright = '', ''

    game = b(requests.get(game_link).text, 'lxml')  # url

    teamleft = game.find('div', class_='live_game_ht').text  # names
    teamright = game.find('div', class_='live_game_at').text

    goals = [goal.text for goal in game.find_all('div', class_="live_game_goal")]  # goals
    left_goal = int(goals[0])
    right_goal = int(goals[1])

    try:
        time = game.find('div', class_='live_game_status')  # time
        if (time is not None) and ('Перерыв' not in time.text):
            time = int(time.text[1:-6])
    except Exception:
        pass

    koeffleft, koeffright = 0, 0
    try:
        koeffs = [koeff.text for koeff in game.find_all('span', class_="koeff")]  # koeff (not always)
        koeffleft, koeffright = float(koeffs[0]), float(koeffs[2])
    except Exception:
        pass

    try:  # Melbet coeff
        Melbet = [i.find_all('div', class_='odds_coeff') for i in game.find_all('div', class_='odds_item odds_logo') if
                  i.find_all('div', class_='odds_coeff') and 'Melbet' in i.text]
        Melbet_left_coeff = Melbet[0][0].text
        Melbet_right_coeff = Melbet[0][2].text
    except Exception:
        pass

    try:  # голы обеих команд
        event_goal_left = list()
        event_goal_right = list()
        all_mins = game.find('div', class_='block_body_nopadding').find_all('div', class_='event_min')
        for i in all_mins:
            try:
                if i.find_previous_sibling('div').find('div',
                                                       class_="event_ht_icon live_goal") or i.find_previous_sibling(
                    'div').find('div', class_="event_ht_icon live_pengoal") or i.find_previous_sibling('div').find(
                    'div', class_="event_ht_icon live_owngoal"):
                    event_goal_left.append(int(i.text[:-1]))
            except Exception:
                pass
            try:
                if i.find_next_sibling('div').find('div', class_="event_at_icon live_goal") or i.find_next_sibling(
                        'div').find('div', class_="event_at_icon live_pengoal") or i.find_next_sibling('div').find(
                    'div', class_="event_at_icon live_owngoal"):
                    event_goal_right.append(int(i.text[:-1]))
            except Exception:
                pass
    except Exception:
        print('Ошибка 1')

    try:
        print(
            f'ИГРА \n {teamleft} {koeffleft} {left_goal} {event_goal_left} \n{time} \n {teamright} {koeffright}  {right_goal} {event_goal_right} \n {game_link} {all_mins}')
    except Exception:
        pass

    try:
        strategy1(koeffleft, koeffright, time, left_goal, right_goal, game_link, teamleft, teamright)
    except Exception:
        pass

    try:
        strategy2(koeffleft, koeffright, left_goal, right_goal, game_link, teamleft, teamright, event_goal_left,
                  event_goal_right)
    except Exception:
        pass

    try:
        strategy3(koeffleft, koeffright, left_goal, right_goal, game_link, teamleft, teamright, event_goal_left,
                  event_goal_right)
    except Exception:
        pass

    check_strategy1()

    check_strategy2()

    check_strategy3()


def strategy1(kl, kr, time, left_goal, right_goal, game_link, teamleft, teamright):  # По стратегии 1
    global game_list
    if ((1.1 <= float(kl) <= 1.25) or (1.1 <= float(kr) <= 1.25)) and 40 >= int(time) >= 10 and left_goal == 0 and right_goal == 0 and (game_link not in game_list) and "(j)" not in game_link:
        game_list.add(game_link)
        text = f'Команда: {teamleft[1:]}Счёт: {left_goal}\nКоф на победу: {kl} \n\n Команда: {teamright[1:]}Счёт: {right_goal}\nКоф на победу: {kr} \n Ссылка на игру: {game_link}\n'
        dict_for_1st_strategy[game_link] = [tgBot.send_message(-1001765456131, text).message_id, text]


def strategy2(kl, kr, left_goal, right_goal, game_link, teamleft, teamright, event_goal_left, event_goal_right):
    global game_list

    if len(event_goal_left) == 3:
        if (event_goal_left[0] < 45 and event_goal_left[1] < 45) and (
                event_goal_left[2] >= 46 and event_goal_left[2] <= 55) and (game_link not in game_list):
            text = f'Команда: {teamleft[1:]}Счёт: {left_goal}\nКоф на победу: {kl} \n\n Команда: {teamright[1:]}Счёт: {right_goal}\nКоф на победу: {kr} \n Ссылка на игру: {game_link}\n По стратегии два в первом и один во втором'
            game_list.add(game_link)
            dict_for_2nd_strategy[game_link] = [tgBot.send_message(-4094235674, text).message_id, text]

    if len(event_goal_right) == 3:
        if (event_goal_right[0] < 45 and event_goal_right[1] < 45) and (
                event_goal_right[2] >= 46 and event_goal_right[2] <= 55) and (game_link not in game_list):
            text = f'Команда: {teamleft[1:]}Счёт: {left_goal}\nКоф на победу: {kl} \n\n Команда: {teamright[1:]}Счёт: {right_goal}\nКоф на победу: {kr} \n Ссылка на игру: {game_link}\n По стратегии два в первом и один во втором'
            game_list.add(game_link)
            dict_for_2nd_strategy[game_link] = [tgBot.send_message(-4094235674, text).message_id, text]


def strategy3(kl, kr, left_goal, right_goal, game_link, teamleft, teamright, event_goal_left, event_goal_right):
    global game_list

    if len(event_goal_left) == 4:
        if (event_goal_left[0] < 45 and event_goal_left[1] < 45 and event_goal_left[2] < 45) and (
                event_goal_left[3] >= 46 and event_goal_left[3] <= 55) and (game_link not in game_list):
            text = f'Команда: {teamleft[1:]}Счёт: {left_goal}\nКоф на победу: {kl} \n\n Команда: {teamright[1:]}Счёт: {right_goal}\nКоф на победу: {kr} \n Ссылка на игру: {game_link}\n По стратегии три в первом и один во втором'
            game_list.add(game_link)
            dict_for_3rd_strategy[game_link] = [tgBot.send_message(-4074671219, text).message_id, text]
    if len(event_goal_right) == 4:
        if (event_goal_right[0] < 45 and event_goal_right[1] < 45 and event_goal_left[2] < 45) and (
                event_goal_right[3] >= 46 and event_goal_right[3] <= 55) and (game_link not in game_list):
            text = f'Команда: {teamleft[1:]}Счёт: {left_goal}\nКоф на победу: {kl} \n\n Команда: {teamright[1:]}Счёт: {right_goal}\nКоф на победу: {kr} \n Ссылка на игру: {game_link}\n По стратегии три в первом и один во втором'
            game_list.add(game_link)
            dict_for_3rd_strategy[game_link] = [tgBot.send_message(-4074671219, text).message_id, text]
def check_strategy1():
    for i in dict_for_1st_strategy:
        left_goal, right_goal, remove_list, game = get_info_to_check(i)
        try:
            time = game.find('div', class_='live_game_status')  # time
            if (time is not None) and ('Перерыв' not in time.text):
                time = int(time.text[1:-6])
                if (left_goal != 0 or right_goal != 0) and time == 45:
                    tgBot.edit_message_text(chat_id=-1001765456131, message_id=dict_for_1st_strategy[i][0],
                                            text=f"{dict_for_1st_strategy[i][1]} \n ✅✅✅")
                    remove_list.append(i)
                elif (left_goal == 0 and right_goal == 0) and time == 45:
                    tgBot.edit_message_text(chat_id=-1001765456131, message_id=dict_for_1st_strategy[i][0],
                                            text=f"{dict_for_1st_strategy[i][1]} \n ⛔⛔⛔")
                    remove_list.append(i)
                else:
                    print("Ошибка чека")
        except Exception:
            print("Ошибка чека")

        for i in remove_list:
            dict_for_1st_strategy.pop(i)

        remove_list.clear()


def check_strategy2():
    for i in dict_for_2nd_strategy:
        left_goal, right_goal, remove_list, game = get_info_to_check(i)
        try:
            time = game.find('div', class_='live_game_status')  # time
            if (time is not None) and ('Перерыв' not in time.text):
                time = int(time.text[1:-6])
                if (left_goal + right_goal) >= 4 and 88 <= time <= 90:
                    tgBot.edit_message_text(chat_id=-4094235674, message_id=dict_for_2nd_strategy[i][0],
                                            text=f"{dict_for_2nd_strategy[i][1]} \n ✅✅✅")
                    remove_list.append(i)
                elif (left_goal + right_goal) <= 4 and 88 <= time <= 90:
                    tgBot.edit_message_text(chat_id=-4094235674, message_id=dict_for_2nd_strategy[i][0],
                                            text=f"{dict_for_2nd_strategy[i][1]} \n ⛔⛔⛔")
                    remove_list.append(i)
                else:
                    print("Ошибка чека")
        except Exception:
            print("Ошибка чека")

        for i in remove_list:
            dict_for_2nd_strategy.pop(i)

        remove_list.clear()


def check_strategy3():
    for i in dict_for_3rd_strategy:
        left_goal, right_goal, remove_list, game = get_info_to_check(i)
        try:
            time = game.find('div', class_='live_game_status')  # time
            if (time is not None) and ('Перерыв' not in time.text):
                time = int(time.text[1:-6])
                if (left_goal + right_goal) >= 5 and 88 <= time <= 90:
                    tgBot.edit_message_text(chat_id=-4074671219, message_id=dict_for_3rd_strategy[i][0],
                                            text=f"{dict_for_3rd_strategy[i][1]} \n ✅✅✅")
                    remove_list.append(i)
                elif (left_goal + right_goal) <= 5 and 88 <= time <= 90:
                    tgBot.edit_message_text(chat_id=-4074671219, message_id=dict_for_3rd_strategy[i][0],
                                            text=f"{dict_for_3rd_strategy[i][1]} \n ⛔⛔⛔")
                    remove_list.append(i)
                else:
                    print("Ошибка чека")
        except Exception:
            print("Ошибка чека")

        for i in remove_list:
            dict_for_3rd_strategy.pop(i)

        remove_list.clear()


def get_info_to_check(i):
    remove_list = list()
    game = b(requests.get(i).text, 'lxml')  # url
    goals = [goal.text for goal in game.find_all('div', class_="live_game_goal")]  # goals
    return int(goals[0]), int(goals[1]), remove_list, game


def start():
    print('blob')
    try:
        while True:
            for i in ['https://soccer365.ru' + link.find('a').get('href') for link in
                      b(requests.get('https://soccer365.ru/online/&tab=1').text, 'lxml').find_all('div',
                                                                                                  class_='game_block online')]:
                get_info_from_game(i)
            sleep(60)
    except Exception:
        start()



start()
