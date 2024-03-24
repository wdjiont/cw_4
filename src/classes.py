import json
import requests
from abc import ABC, abstractmethod


class AbcAPI(ABC):
    """ Абстрактный класс """
    @abstractmethod
    def get_vacancies(self, *args, **kwargs):
        pass


class HeadHunter(AbcAPI):
    """ Сохраняет вакансии по поисковому запросу в json файл """
    def __init__(self, url):
        self.url = url

    def get_vacancies(self, key):
        """ Получает вакансии по ключевому слову """
        res = requests.get(self.url, params={'text': key, 'per_page': 100})
        return res.json()

    @staticmethod
    def get_json(res, file_name):
        """ Записывает вакансии по ключевому слову в json файл """
        with open(file_name, "w", encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=4)


class Vacancies:
    """ Класс для взаимодействия с вакансиями """

    def __init__(self, name, city, url, salary, responsibility='Не указано', requirement='Не указаны'):
        self.name = name
        self.url = url
        self.city = city
        self.salary = salary
        self.responsibility = responsibility
        self.requirement = requirement

    def __repr__(self):
        return f"{self.name}, {self.city}, {self.url}, {self.salary}, {self.responsibility}, {self.requirement}"

    @staticmethod
    def get_list(file):
        """ Создает файл json с экзеплярами класса """
        zero_list = []
        with open(file, 'r', encoding='utf-8') as f:
            t = json.load(f)
        for exm in t['items']:
            if exm['salary'] is None:
                exm['salary'] = 0
            else:
                if exm['salary']['from'] is None and exm['salary']['to'] is not None:
                    exm['salary'] = exm['salary']['to']
                elif exm['salary']['from'] is not None and exm['salary']['to'] is None:
                    exm['salary'] = exm['salary']['from']
                elif exm['salary']['from'] is not None and exm['salary']['to'] is not None:
                    exm['salary'] = exm["salary"]["from"]
            example = Vacancies(exm['name'], exm['area']['name'], exm['alternate_url'], exm['salary'], exm['snippet']['responsibility'], exm['snippet']['requirement'])
            zero_list.append(example)
        return zero_list

    def __gt__(self, other):
        """ Сравнивает вакансии по зарплате """
        if other.salary is not None and self.salary is not None:
            if self.salary['currency'] == other.salary['currency']:
                if self.salary['from'] > other.salary['from']:
                    return f"{self.name} - {self.salary['from']} {self.salary['currency']}"
                else:
                    return f"{other.name} - {other.salary['from']} {other.salary['currency']}"
            else:
                return "Невозможно сравнить разные валюты"
        else:
            return "Зарплата не указана"


class JSONAbc(ABC):
    @abstractmethod
    def add_vac(self, *args, **kwargs):
        pass

    def get_info(self):
        pass

    def del_vac(self):
        pass


class SaveVac(JSONAbc):

    @staticmethod
    def save_json(v):
        """ Перезаписывает json файл в читаемом для пользователя виде """
        vac_exm_list = []
        for i in v:
            vac_exm_list.append({'Название вакансии': i.name, 'Город': i.city, 'Ссылка': i.url,
                           'Зарплата': i.salary, 'Обязанности': i.responsibility, 'Требования': i.requirement})

        with open('filtred.json', 'w', encoding='utf=8') as f:
            json.dump(vac_exm_list, f, ensure_ascii=False, indent=4)

    @staticmethod
    def add_vac(vacancy, file):
        """ Добавляет вакансию в отсортированный json файл """
        with open(file, 'r+', encoding='utf-8') as f:
            file_data = json.load(f)
            file_data.append(vacancy)
            f.seek(0)
            json.dump(file_data, f, ensure_ascii=False, indent=4)

    def get_info(self):
        pass

    def del_vac(self):
        pass

    @staticmethod
    def get_vacancies_by_filter(key_word, file):
        user_list = []
        with open(file, 'r', encoding='utf=8') as f:
            text = json.load(f)
        for i in text:
            if i['Требования'] is not None or i['Требования'] is not None:
                if key_word in i['Название вакансии'] or key_word in i['Требования']:
                    user_list.append(i)
        return user_list

    @staticmethod
    def sort_by_salary(n, file):
        with open(file, 'r', encoding='utf=8') as f:
            text = json.load(f)
            sorted_list = sorted(text, key=lambda x: x['Зарплата'], reverse=True)
            for i in sorted_list[0:n]:
                for k, v in i.items():
                    print(f'{k}:{v}')
                print()
