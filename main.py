import requests
import telebot
import asyncio
from time import sleep
from bs4 import BeautifulSoup as b

game_list = set()
online_games_list = list()
aboba_list = set()
tgBot = telebot.TeleBot('5061487172:AAFgTi1TN_WfNAJu3jQyb666MWosv6JJpms')


async def find_matches():
    global online_games_list
    online_games_list = list()
    online_games_list = ['https://soccer365.ru' + link.find('a').get('href') for link in
                         b(requests.get('https://soccer365.ru/online/&tab=1').text, 'lxml').find_all('div',
                                                                                                     class_='game_block online')]
    for i in online_games_list:
        task6 = asyncio.create_task(get_info_from_game(i))
        await task6
    print(online_games_list)
    await asyncio.sleep(120)


async def get_info_from_game(game_link):
    global event_goal_left, time, koeffright, event_goal_right, all_mins, koeffleft

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
                    'div').find('div', class_="event_ht_icon live_pengoal") or i.find_previous_sibling('div').find('div', class_="event_ht_icon live_owngoal"):
                    event_goal_left.append(int(i.text[:-1]))
            except Exception:
                pass
            try:
                if i.find_next_sibling('div').find('div', class_="event_at_icon live_goal") or i.find_next_sibling(
                        'div').find('div', class_="event_at_icon live_pengoal") or i.find_next_sibling('div').find('div', class_="event_at_icon live_owngoal"):
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
        task31 = asyncio.create_task(
            strategy1(koeffleft, koeffright, time, left_goal, right_goal, game_link, teamleft, teamright))
        await task31
    except Exception:
        pass

    try:
        task2 = asyncio.create_task(
            strategy3(koeffleft, koeffright, left_goal, right_goal, game_link, teamleft, teamright, event_goal_left,
                      event_goal_right))
        await task2
    except Exception:
        pass

    try:
        task3 = asyncio.create_task(strategy3(koeffleft, koeffright, left_goal, right_goal, game_link, teamleft, teamright, event_goal_left,
                  event_goal_right))
        await task3
    except Exception:
        pass


async def strategy1(kl, kr, time, left_goal, right_goal, game_link, teamleft, teamright):  # По стратегии 1
    global game_list
    if ((1.1 <= float(kl) <= 1.5) or (1.1 <= float(kr) <= 1.5)) and 30 >= int(
            time) >= 10 and left_goal == 0 and right_goal == 0 and (game_link not in game_list):
        tgBot.send_message(-1001765456131,
                           f'Команда: {teamleft[1:]}Счёт: {left_goal}\nКоф на победу: {kl} \n\n Команда: {teamright[1:]}Счёт: {right_goal}\nКоф на победу: {kr} \n Ссылка на игру: {game_link}\n')
        game_list.add(game_link)


async def strategy2(kl, kr, left_goal, right_goal, game_link, teamleft, teamright, event_goal_left, event_goal_right):
    global game_list

    if len(event_goal_left) == 3:
        if (event_goal_left[0] < 45 and event_goal_left[1] < 45) and (event_goal_left[2] >= 45 and event_goal_left[2] <= 55) and (game_link not in game_list):
            tgBot.send_message(-1001765456131,
                               f'Команда: {teamleft[1:]}Счёт: {left_goal}\nКоф на победу: {kl} \n\n Команда: {teamright[1:]}Счёт: {right_goal}\nКоф на победу: {kr} \n Ссылка на игру: {game_link}\n По стратегии два в первом и один во втором')
            game_list.add(game_link)
    if len(event_goal_right) == 3:
        if (event_goal_right[0] < 45 and event_goal_right[1] < 45) and (event_goal_right[2] >= 45 and event_goal_right[2] <= 55) and (game_link not in game_list):
            tgBot.send_message(-1001765456131,
                               f'Команда: {teamleft[1:]}Счёт: {left_goal}\nКоф на победу: {kl} \n\n Команда: {teamright[1:]}Счёт: {right_goal}\nКоф на победу: {kr} \n Ссылка на игру: {game_link}\n По стратегии два в первом и один во втором')
            game_list.add(game_link)

async def strategy3(kl, kr, left_goal, right_goal, game_link, teamleft, teamright, event_goal_left, event_goal_right):
    global game_list

    if len(event_goal_left) == 4:
        if (event_goal_left[0] < 45 and event_goal_left[1] < 45 and event_goal_left[2] < 45) and (event_goal_left[3] >= 45 and event_goal_left[3] <= 55)and (game_link not in game_list):
            tgBot.send_message(-1001765456131,
                               f'Команда: {teamleft[1:]}Счёт: {left_goal}\nКоф на победу: {kl} \n\n Команда: {teamright[1:]}Счёт: {right_goal}\nКоф на победу: {kr} \n Ссылка на игру: {game_link}\n По стратегии два в первом и один во втором')
            game_list.add(game_link)
    if len(event_goal_right) == 4:
        if (event_goal_right[0] < 45 and event_goal_right[1] < 45 and event_goal_left[2] < 45) and (event_goal_right[3] >= 45 and event_goal_right[3] <= 55) and (game_link not in game_list):
            tgBot.send_message(-1001765456131,
                               f'Команда: {teamleft[1:]}Счёт: {left_goal}\nКоф на победу: {kl} \n\n Команда: {teamright[1:]}Счёт: {right_goal}\nКоф на победу: {kr} \n Ссылка на игру: {game_link}\n По стратегии два в первом и один во втором')
            game_list.add(game_link)

async def check():
    await asyncio.sleep(600)
    global game_list

    for n, i in enumerate(aboba_list):
        game = b(requests.get(i).text, 'lxml')  # url

        goals = [goal.text for goal in game.find_all('div', class_="live_game_goal")]  # goals
        left_goal = int(goals[0])
        right_goal = int(goals[1])

        try:
            time = game.find('div', class_='live_game_status')  # time
            if (time is not None) and ('Перерыв' not in time.text):
                time = int(time.text[1:-6])
        except Exception:
            pass

        if (left_goal != 0 or left_goal != 0) and time > 30:
            tgBot.send_message(-1001765456131, f'{i} +')
            game_list.remove(game_list[i])
        elif (left_goal == 0 or left_goal == 0) and time > 30:
            tgBot.send_message(-1001765456131, f'{i} -')
            game_list.remove(game_list[i])
        else:
            print("Ошибка чека")




async def start():
    print('blob')
    try:
        while True:
            taskFM = asyncio.create_task(find_matches())
            await taskFM
            taskCheck = asyncio.create_task(check())
            await taskCheck
    except Exception:
        await asyncio.create_task(start())


asyncio.run(start())


