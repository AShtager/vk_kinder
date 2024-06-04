import os
import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from dotenv import load_dotenv
load_dotenv()

vk_token = os.getenv("TOKEN_VK")

authorize = vk_api.VkApi(token=vk_token)
longpoll = VkLongPoll(authorize)
search_parameters = {"city": "", "gender": "", "age": ""}


class ButtonVK():
    # keyboard = VkKeyboard(one_time=True)
    lets_go = "Приступим"
    finish = "Завершить"
    confirmation = "Да верно"
    modify = "Изменить"
    gender_m = "Парень"
    gender_w = "Девушка"
    city = "Город"
    gender = "Пол"
    age = "Возраст"
    next_user = "Следующий"
    favourites = "Фавориты"
    add_favour = "Добавить в фавориты"
    watch_all = "Посмотрим всех"


def write_message(sender, message, keyboard=None):
    """
    отправка сообщения собеседнику sender=id пользователя, message=сообщение пользователю в чат, 
    keyboard нужно добавлять тогда когда хотим добавить кнопки
    """
    param = {
        "user_id": sender,
        "message": message,
        "random_id": get_random_id(),
    }
    if keyboard is not None:
        param["keyboard"] = keyboard.get_keyboard()

    authorize.method("messages.send", param)


def start(user_id):
    """
    отправка кнопки предлогающей начать подбор
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(ButtonVK.lets_go, VkKeyboardColor.PRIMARY)
    keyboard.add_button(ButtonVK.finish, VkKeyboardColor.NEGATIVE)
    write_message(user_id, "Поднимем демографию!!!", keyboard)


def finish(user_id):
    """
    отправка сообщения о завершении сеанса
    """
    write_message(user_id, "До новых встреч")


def city(user_id):
    """
    отправка сообщения с просьбой ввести город
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(ButtonVK.finish, VkKeyboardColor.PRIMARY)
    write_message(user_id, "Введите город", keyboard)


def city_confirm(user_id, city):
    """
    кнопка для подтверждения или изменения города
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(ButtonVK.confirmation, VkKeyboardColor.PRIMARY)
    keyboard.add_button(ButtonVK.modify, VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(ButtonVK.finish, VkKeyboardColor.NEGATIVE)
    write_message(user_id, f"Начать поиск в городе {city.capitalize()}?", keyboard)


def gender(user_id):
    """
    отправка кнопки для выбора пола
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(ButtonVK.gender_m, VkKeyboardColor.PRIMARY)
    keyboard.add_button(ButtonVK.gender_w, VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(ButtonVK.finish, VkKeyboardColor.NEGATIVE)
    write_message(user_id, "Кто нужен?", keyboard)


def age(user_id):
    """
    отправка сообщения с запросом возраста
    """
    write_message(user_id, "укажите возраст")


def data_confirm(user_id, gender, city, age):
    """
    отправка кнопок для изменения или подтверждения
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(ButtonVK.confirmation, VkKeyboardColor.PRIMARY)
    keyboard.add_button(ButtonVK.modify, VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(ButtonVK.finish, VkKeyboardColor.NEGATIVE)
    write_message(user_id, f"Ищем {gender} из города {city.capitalize()} возрастом {age}", keyboard)


def data_modify(user_id, city, age, gender):
    """
    отправка кнопок для выбора изменения
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(ButtonVK.city, VkKeyboardColor.PRIMARY)
    keyboard.add_button(ButtonVK.age, VkKeyboardColor.PRIMARY)
    keyboard.add_button(ButtonVK.gender, VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(ButtonVK.finish, VkKeyboardColor.NEGATIVE)
    write_message(user_id, "Что изменить?", keyboard)


def navigation(user_id):
    """
    отправка кнопок навигации для выбора действий 
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(ButtonVK.next_user, VkKeyboardColor.PRIMARY)
    keyboard.add_button(ButtonVK.add_favour, VkKeyboardColor.PRIMARY)
    keyboard.add_button(ButtonVK.favourites, VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(ButtonVK.finish, VkKeyboardColor.NEGATIVE)
    write_message(user_id, "Ну как тебе?", keyboard)


def main():
    flag = ""
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.message
            user_id = event.user_id
            if msg == "Начать" and flag == "":
                start(user_id)
                flag = "start"
            if msg == ButtonVK.finish:
                finish(user_id)
                flag = ""
            elif msg == ButtonVK.lets_go:
                # удаляем бд
                # создаем бд
                city(user_id)
                flag = "city"
            elif flag == "city":
                city_confirm(user_id, msg)
                flag = msg
            elif msg == ButtonVK.confirmation and flag != "data modify":
                city_search = flag
                search_parameters["city"] = city_search.capitalize()
                flag = "gender"
                gender(user_id)
            elif msg == ButtonVK.city:
                city(user_id)
                if search_parameters["gender"] == "":
                    flag = "city"
                else:
                    flag = "modify city"
            elif msg == ButtonVK.gender_m and flag != "modify gender":
                gender_search = msg
                search_parameters["gender"] = "men"
                age(user_id)
                flag = "age"
            elif msg == ButtonVK.gender_w and flag != "modify gender":
                gender_search = msg
                search_parameters["gender"] = "women"
                age(user_id)
                flag = "age"
            elif flag == "age":
                try:
                    age_search = msg.strip()
                    search_parameters["age"] = age_search
                    flag = "data modify"
                    data_confirm(
                        user_id=user_id,
                        city=search_parameters["city"],
                        gender=gender_search,
                        age=search_parameters["age"],
                    )
                except ValueError:
                    write_message(user_id, "Технические неполадки")
                    age(user_id)
            elif msg == ButtonVK.modify:
                data_confirm(user_id)
            elif msg == ButtonVK.city:
                city(user_id)
                flag = "modify city"
            elif flag == "modify city":
                flag = "data modify"
                new_city = msg
                city_confirm(user_id, msg)
            elif msg == ButtonVK.confirmation and flag == "data modify":
                city_search = new_city
                search_parameters["city"] = city_search.capitalize()
                data_modify(
                    user_id=user_id,
                    city=search_parameters["city"],
                    gender=gender_search,
                    age=search_parameters["age"]
                )
            elif msg == ButtonVK.age:
                age(user_id)
                flag = "age"
            elif msg == ButtonVK.gender:
                flag = "modify gender"
                gender(user_id)
            elif msg == ButtonVK.gender_m and flag == "modify gender":
                gender_search = msg
                search_parameters["gender"] = "men"
                data_modify(
                    user_id=user_id,
                    city=search_parameters["city"],
                    age=search_parameters["age"],
                    gender=gender_search,
                )
            elif msg == ButtonVK.gender_w and flag == "modify gender":
                gender_search = msg
                search_parameters["gender"] = "women"
                data_modify(
                    user_id=user_id,
                    city=search_parameters["city"],
                    age=search_parameters["age"],
                    gender=gender_search
                )
            elif msg == ButtonVK.watch_all:
                # логика вывода пользователей
                pass
            elif msg == ButtonVK.next_user:
                # логика следующего вывода
                pass
            elif msg == ButtonVK.add_favour:
                # логика добавления в фавориты
                pass
            elif msg == ButtonVK.favourites:
                # логика вывода фаворитов
                pass


if __name__ == "__main__":
    print("Бот запущен!")
    main()
