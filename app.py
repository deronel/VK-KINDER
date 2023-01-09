from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_user import VK
from funck_for_BD import pretendents_output, favourites_insert, favourites_output
from vk_api.exceptions import ApiError
from token_for_vk import token_public, tokenVk


vk = vk_api.VkApi(token=token_public)
longpoll = VkLongPoll(vk)
vk_user = VK(tokenVk)


def write_msg(user_id, message, keyboard=None):
    '''Функция отправляет сообщения в чат бота. На вход принимает id пользователя, текст сообщения.'''
    post = {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7)
    }

    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    else:
        post = post

    vk.method('messages.send', post)


if __name__ == "__main__":

    num_pr = 0  # нумерация для всех претендентов
    num_f = 0  # нумерация для избранных
    flag_fav = 0  # флаг того, что листаем фаворитов
    len_fav = 0  # количество фаворитов
    link_profile = 'https://vk.com/id'

    print('Напиши привет в чат...')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                if request.lower() == "привет":
                    print('Идет поиск претендентов, пока ждем...')
                    user_name = vk_user.users_info(event.user_id)
                    print('Готово. Можно нажать - Начать')
                    keyboard = VkKeyboard()
                    keyboard.add_button('Начать', color=VkKeyboardColor.NEGATIVE)
                    keyboard.add_button('Следующий', color=VkKeyboardColor.POSITIVE)
                    keyboard.add_button('В избранное', color=VkKeyboardColor.NEGATIVE)
                    keyboard.add_line()
                    keyboard.add_button('Посмотреть избранное', color=VkKeyboardColor.SECONDARY)
                    write_msg(event.user_id,
                              f"Привет, {user_name}! Мы хотим помочь тебе найти вторую половинку, нажми Начать", keyboard)
                elif request.lower() == "начать":
                    pretendets = pretendents_output(event.user_id)
                    write_msg(event.user_id,
                              f'{pretendets[num_pr][1]} ' f'{pretendets[num_pr][2]} \n' f'Ссылка на страничку: {link_profile}{pretendets[num_pr][0]} \n' f'Самые популярные фото странички: \n ' f'1. {pretendets[num_pr][3]} \n' f' 2. {pretendets[num_pr][4]} \n'  f'3. {pretendets[num_pr][5]} \n '
                              f'Для перехода к следующему претенденту нажми - Следующий,\n'
                              f'Для добавления претендента в избранное нажми - В избранное.')
                elif request.lower() == "следующий":
                    if flag_fav == 0:
                        num_pr += 1

                        try:
                            write_msg(event.user_id,
                                      f'{pretendets[num_pr][1]} ' f'{pretendets[num_pr][2]} \n' f'Ссылка на страничку: {link_profile}{pretendets[num_pr][0]} \n' f'Самые популярные фото странички: \n ' f'1. {pretendets[num_pr][3]} \n' f' 2. {pretendets[num_pr][4]} \n'  f'3. {pretendets[num_pr][5]} \n '
                                      f'Для перехода к следующему претенденту нажми - Следующий,\n'
                                      f'Для добавления претендента в избранное нажми - В избранное.')
                        except IndexError:
                            num_pr = 0
                            write_msg(event.user_id,
                                      f"Пока это все претенденты, можете начать сначала листать, нажмите кнопку Следующий")
                        except NameError:
                            write_msg(event.user_id, "Сначала необходимо нажать кнопку Начать")

                    else:
                        num_f += 1
                        favorites = favourites_output(event.user_id)
                        len_fav = len(favorites)  # количество фаворитов
                        if num_f < len_fav:
                            write_msg(event.user_id,
                                      f'{favorites[num_f][1]} ' f'{favorites[num_f][2]} \n' f'Ссылка на страничку: {link_profile}{favorites[num_f][0]} \n' f'Самые популярные фото странички: \n ' f'1. {favorites[num_f][3]} \n' f' 2. {favorites[num_f][4]} \n'  f'3. {favorites[num_f][5]} '
                                      f'Для перехода к следующему избранному нажми - Следующий.\n')
                        else:
                            num_f = 0
                            flag_fav = 0
                            write_msg(event.user_id,
                                      f"Пока это все избранные.\n Нажми Начать для просмотра претендентов.")

                elif request.lower() == "в избранное":
                    try:
                        favourites_insert(event.user_id, pretendets[num_pr][0], pretendets[num_pr][1], pretendets[num_pr][2],
                                          pretendets[num_pr][3], pretendets[num_pr][4], pretendets[num_pr][5])
                        write_msg(event.user_id,
                                  f'Претендент {pretendets[num_pr][1]} {pretendets[num_pr][2]} добавлен в избранное.\n'
                                  f'Для просмотра избранных претендентов нажми - Посмотреть избранное.')
                    except NameError:
                        write_msg(event.user_id, "Некого добавлять в Избранное, сначала необходимо нажать кнопку Начать")

                elif request.lower() == "посмотреть избранное":
                    try:
                        favorites = favourites_output(event.user_id)
                        len_fav = len(favorites)  # количество фаворитов
                        flag_fav = 1
                        write_msg(event.user_id,
                                  f'{favorites[num_f][1]} ' f'{favorites[num_f][2]} \n' f'Ссылка на страничку: {link_profile}{favorites[num_f][0]} \n' f'Самые популярные фото странички: \n ' f'1. {favorites[num_f][3]} \n' f' 2. {favorites[num_f][4]} \n'  f'3. {favorites[num_f][5]} \n '
                                  f'Для перехода к следующему избранному нажми - Следующий.\n')
                    except IndexError:
                        num_f = 0
                        flag_fav = 0
                        write_msg(event.user_id, "Избранных пока нет.")

                else:
                    write_msg(event.user_id, "Не понял вашего ответа...")