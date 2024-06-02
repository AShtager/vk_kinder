import os
import requests
from dotenv import load_dotenv


class VKAPIUser:
    """
    Класс для работы с API VK
    """
    load_dotenv()
    token = os.getenv('USER_TOKEN')
    user_id = os.getenv('USER_ID')
    base_url = 'https://api.vk.com/method/'

    def __init__(self, token, user_id):
        """
        Инициализация переменных
        """
        self.token = token
        self.user_id = user_id

    def get_params(self):
        """
        Параметры для запроса
        """
        return {
            'access_token': self.token,
            'v': '5.131',
            'user_id': self.user_id
        }

    def build_url(self, method):
        """
        Построение URL ссылки для работы с API
        """
        return f'{self.base_url}/{method}'

    def get_users_info(self):
        """
        Получение информации о пользователе
        """
        method = 'users.get'
        url = self.build_url(method)
        params = self.get_params()
        params.update({'user_ids': self.user_id, 'fields': 'bdate, city, sex'})
        response = requests.get(url, params=params)
        return response.json()['response']

    def get_city_info(self, city_id):
        """
        Получение информации о городе
        """
        method = 'database.getCitiesById'
        url = self.build_url(method)
        params = self.get_params()
        params.update({'country_id': 1, 'count': 1000, 'need_all': 1, 'q': city_id})
        response = requests.get(url, params=params)
        return response.json()['response']

    def find_users(self, age, city_id, sex):
        """
        Поиск пользователей по параметрам
        """
        method = 'users.search'
        url = self.build_url(method)
        params = self.get_params()
        params.update({'count': 1000, 'city': city_id, 'age_from': age, 'age_to': age, 'sex': sex})
        response = requests.get(url, params=params)
        return response.json()['response']

    def get_user_photos(self, user_id):
        """
        Получение фотографий пользователя
        """
        method = 'photos.get'
        url = self.build_url(method)
        params = self.get_params()
        params.update({'owner_id': user_id, 'album_id': 'profile', 'extended': 1})
        response = requests.get(url, params=params)
        return response

    def get_max_quality_photos(self, owner_id):
        """
        Получение максимальной качественной фотографии пользователя
        """
        reply = self.get_user_photos(owner_id)
        foto_list = []
        try:
            list_foto_all_info = reply.json()['response']['items']
        except:
            status = 'error'
            print(f'Ошибка: {reply.json()["error"]["error_msg"]}')
        else:
            status = 'success'
            vk_photo_sizes = {'s': 0, 'm': 1, 'x': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'y': 7, 'z': 8, 'w': 9}
            for foto_all_info in list_foto_all_info:
                max_photo_size = max(foto_all_info['sizes'], key=lambda x: vk_photo_sizes[x['type']])
                max_photo_size['count_likes'] = foto_all_info["likes"]["count"]
                foto_list.append(max_photo_size)
        return get_url_photos(get_three_popular_photos(foto_list))


def get_three_popular_photos(photo_list: list):
    """
    Получение трех популярных фотографий пользователя
    """
    photo_list.sort(key=lambda x: x['count_likes'], reverse=True)
    return photo_list[:3]


def get_url_photos(photo_list: list):
    """
    Получение URL фотографий
    """
    final_photo_list = []
    for photo in photo_list:
        final_photo_list.append(photo['url'])
    return final_photo_list
