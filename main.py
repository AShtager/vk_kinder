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
keyboard = VkKeyboard(one_time=True)


class ButtonVK():
    lets_go = "Приступим"
    start_searching = "Начать поиск"
    next_person = "Cледующий"
    keep_person = "Оставить в фаворитах"
    favourites_list = "Показать всех фаворитов"
    gender_m = "Парень"
    gender_f = "Девушка"


def write_message(sender, message, keyboard=None):
    authorize.method("messages.send", {"user_id": sender, "message": message,
                     "random_id": get_random_id(), "keyboard": keyboard.get_keyboard()})


def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            reseived_message = event.text.capitalize()
            sender = event.user_id
            if reseived_message == "Начать":
                keyboard.add_button(ButtonVK.lets_go, color=VkKeyboardColor.PRIMARY)
                write_message(sender, "Добро пожаловать на шоу Давай поженимся", keyboard)
            else:
                write_message(sender, "Я пока ни чего не умею", keyboard)


if __name__ == "__main__":
    print("Бот запущен!")
    main()
