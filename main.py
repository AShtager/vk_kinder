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
search_parameters = {"city": "", "gender": "", "age": ""}  # параметры которые передадим в функцию поиска


class ButtonVK():
    start = "Начнем подбор!"
    finish = "Завершить"
    lets_go = "Поднимем демографию"
    enter_city = "Введите город"
    right_city = "Город указан верно"
    modify_city = "Изменить город"
    boy = "Парень"
    girl = "Девушка"
    all_true = "Все верно"
    change_parameters = "Изменить параметры"
    city = "Город"
    age = "Возраст"
    gender = "Пол"
    next = "Следующий"
    add_favourites = "Добавить в фавориты"
    all_fovourites = "Все фавориты"
    display = "Начать показ"


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
    keyboard.add_button(ButtonVK.start, VkKeyboardColor.PRIMARY)
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
    keyboard.add_button(ButtonVK.right_city, VkKeyboardColor.PRIMARY)
    keyboard.add_button(ButtonVK.modify_city, VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(ButtonVK.finish, VkKeyboardColor.NEGATIVE)
    write_message(user_id, f"Начать поиск в городе {city.capitalize()}?", keyboard)


def gender(user_id):
    """
    отправка кнопки для выбора пола
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(ButtonVK.boy, VkKeyboardColor.PRIMARY)
    keyboard.add_button(ButtonVK.girl, VkKeyboardColor.PRIMARY)
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
    keyboard.add_button(ButtonVK.all_true, VkKeyboardColor.PRIMARY)
    keyboard.add_button(ButtonVK.change_parameters, VkKeyboardColor.PRIMARY)
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
    keyboard.add_button(ButtonVK.next, VkKeyboardColor.PRIMARY)
    keyboard.add_button(ButtonVK.add_favourites, VkKeyboardColor.PRIMARY)
    keyboard.add_button(ButtonVK.all_fovourites, VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(ButtonVK.finish, VkKeyboardColor.NEGATIVE)
    write_message(user_id, "Ну как тебе?", keyboard)


def main():
    flag = ""
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.message
            user_id = event.user_id
            if msg == "Начать":
                start(user_id)

            elif msg == ButtonVK.finish:
                finish(user_id)

            elif msg == ButtonVK.start:
                # удаляем бд
                # создаем бд
                city(user_id)
                flag = "city"

            elif flag == "city":
                city_confirm(user_id, msg)
                flag = msg

            elif msg == ButtonVK.right_city and flag != "data confirm":
                city_search = flag
                search_parameters["city"] = city_search.capitalize()
                flag = "gender"
                gender(user_id)

            elif msg == ButtonVK.modify_city:
                city(user_id)
                if search_parameters["gender"] == "":
                    flag = "city"
                else:
                    flag = "modify city"

            elif msg == ButtonVK.boy and flag != "modify gender":
                gender_search = msg
                search_parameters["gender"] = "men"  # возможно вместо women нужно указать что то другое согласно apivk
                age(user_id)
                flag = "age"

            elif msg == ButtonVK.girl and flag != "modify gender":
                gender_search = msg
                # возможно вместо women нужно указать что то другое согласно apivk
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

            elif msg == ButtonVK.change_parameters:
                data_modify(user_id)

            elif msg == ButtonVK.city:
                city(user_id)
                flag = "modify city"

            elif flag == "modify city":
                flag = "data modify"
                new_city = msg
                city_confirm(user_id, msg)

            elif msg == ButtonVK.right_city and flag == "data modify":
                city_search = new_city
                search_parameters["city"] = city_search.capitalize()
                data_confirm(
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

            elif msg == ButtonVK.boy and flag == "modify gender":
                gender_search = msg
                search_parameters["gender"] = "men"
                data_confirm(
                    user_id=user_id,
                    city=search_parameters["city"],
                    age=search_parameters["age"],
                    gender=gender_search,
                )

            elif msg == ButtonVK.girl and flag == "modify gender":
                gender_search = msg
                search_parameters["gender"] = "women"
                data_confirm(
                    user_id=user_id,
                    city=search_parameters["city"],
                    age=search_parameters["age"],
                    gender=gender_search
                )

            elif msg == ButtonVK.display:
                # логика вывода пользователей
                pass

            elif msg == ButtonVK.next:
                # логика следующего вывода
                pass

            elif msg == ButtonVK.add_favourites:
                # логика добавления в фавориты
                pass

            elif msg == ButtonVK.all_fovourites:
                # логика вывода фаворитов
                pass


if __name__ == "__main__":
    print("Бот запущен!")
    main()
