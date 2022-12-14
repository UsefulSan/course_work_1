import json
import re
from operator import itemgetter

from bs4 import BeautifulSoup

from classes import HH, Superjob, Vacancy


def save_vacs(data: list) -> None:
    """
    Сохраняет обработанные вакансии в тхт файл
    :param data: принимаемые данные
    """
    with open('vacancies.txt', 'a', encoding='utf-8') as file:
        for d in data:
            file.write(d.__repr__() + '\n')


def get_hh_vac(req_text: str, how_many: str) -> None:
    """
    Забирает данные с сайта HH и обрабатывает их
    :param req_text: наименование профессии
    :param how_many: количество обрабатываемых вакансий
    """
    hh = HH(req_text, how_many)
    vacancies = []
    for page in range(hh.iter):
        data = hh.get_request(page)
        json_res = json.loads(data.text)
        for vac in json_res['items']:
            name = vac['name']
            reference = vac['alternate_url']
            if vac['snippet']['requirement'] and vac['snippet']['responsibility']:
                description = vac['snippet']['requirement'] + vac['snippet']['responsibility']
            else:
                try:
                    description = vac['snippet']['requirement']
                except:
                    description = vac['snippet']['responsibility']
            try:
                salary = vac['salary']['from']
            except:
                salary = 0
            vacancies.append(Vacancy(name, reference, description, salary))
        save_vacs(vacancies)


def get_sj_vac(name_job: str) -> None:
    """
    Забирает данные с сайта Superjob и обрабатывает их
    :param name_job: наименование профессии
    """
    vac = []
    sj = Superjob('python')
    response = sj.get_request()
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('span', class_="_9fIP1 _249GZ _1jb_5 QLdOc")
    title = soup.find_all('span', class_="_9fIP1 _249GZ _1jb_5 QLdOc")
    description = soup.find_all('span', class_="_1Nj4W _249GZ _1jb_5 _1dIgi _3qTky")
    salary = soup.find_all('span', class_="_2eYAG _1nqY_ _249GZ _1jb_5 _1dIgi")
    for i in range(0, len(quotes)):
        name = title[i].find('a', href=True)
        vac.append(Vacancy(quotes[i].text, name['href'], description[i].text, (re.sub('[^0-9\—]', '', salary[i].text))))
    save_vacs(vac)


def read_all():
    """
    Читает файл vacancies.txt и выводит отформатированные все строки
    """
    with open('vacancies.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line_list = line.split('|')
            print(line_list[0].replace("'", ""), '\n', line_list[1], '\n', line_list[2], '\n',
                  line_list[3].replace("'", ""), sep='')


def top_10():
    """
    Читает файл vacancies.txt и выводит топ 10 вакансий отсортированных по наибольшей заработной плате
    :return:
    """
    with open('vacancies.txt', 'r', encoding='utf-8') as file:
        some_list = []
        for line in file:
            line_list = line.split('|')
            line_list[0] = line_list[0].replace("'", "")
            try:
                line_list[3] = int(line_list[3].replace("'", ''))
            except ValueError:
                try:
                    line_list[3] = int(line_list[3].split('—')[0])
                except ValueError:
                    line_list[3] = 0
            some_list.append(line_list)
        sorted_list = sorted(some_list, key=itemgetter(3), reverse=True)
        for i in range(10):
            for list in sorted_list[i]:
                print(list)
            print('\n')
