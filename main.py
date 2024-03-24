from src.classes import HeadHunter, Vacancies, SaveVac


def user_interaction():
    user_vacancy = input('Введите вакансию для поиска на сайте hh.ru: \n')
    hh = HeadHunter('https://api.hh.ru/vacancies')
    user_keyword = input('Введите ключевое слово для поиска по вакансиям: \n').title()
    salary_top = int(input('Введите количество вакансий отсортированных по зарплате:\n'))
    vacancies = hh.get_vacancies(user_vacancy)
    hh.get_json(vacancies, 'vacancies.json')
    sorted_vacs = Vacancies.get_list('vacancies.json')
    SaveVac.save_json(sorted_vacs)
    SaveVac.get_vacancies_by_filter(user_keyword, 'filtred.json')
    SaveVac.sort_by_salary(salary_top, 'filtred.json')


if __name__ == "__main__":
    user_interaction()
