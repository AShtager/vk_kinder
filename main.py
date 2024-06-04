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


class ButtonVK():
    # keyboard = VkKeyboard(one_time=True)
    lets_go = "Приступим"
    finish = "Завершить"
    confirmation = "Да верно"
    modify = "Изменить"
    gender_m = "Парень"
    gender_f = "Девушка"
    city = "Город"
    gender = "Пол"
    age = "Возраст"
    next_user = "Следующий"
    favourites = "Фавориты"
    add_favour = "Добавить в фавориты"


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
    keyboard.add_button(ButtonVK.gender_f, VkKeyboardColor.PRIMARY)
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


def data_modify(user_id):
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


if __name__ == "__main__":
    print("Бот запущен!")