import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import json

def parse_hh():
    """
    Функция парсинга вакансий на сайте headhunter
    Ищем вакансии, у которых в описании есть ключевые слова "Django" и "Flask"
    """
    url = 'https://hh.ru/search/vacancy'
    headers = Headers(browser='Firefox', os='Win')
    headers_data = headers.generate()
    params = {
        'area': (1, 2),
        'text': 'python django flask',
        'page': 0,
        'items_on_page': 20
    }

    response = requests.get(url=url, params=params, headers=headers_data).text
    main_page_soup = BeautifulSoup(response, 'lxml')
    div_vanacy_list = main_page_soup.find('div', id='a11y-main-content')
    div_item_tags = div_vanacy_list.find_all('div', class_='serp-item')
    vacancies_list = []

    for vacancy in div_item_tags:
        h3_tag = vacancy.find('h3')
        span = h3_tag.find('span')
        link = span.find('a', class_="serp-item__title").get('href')
        salary_tag = vacancy.find('span', class_="bloko-header-section-3")
        if salary_tag == None:
            salary = 'Зарплата не указана'
        else:
            salary = salary_tag.text.replace('\u202f', '')
        employer = vacancy.find('div', class_='vacancy-serp-item__meta-info-company').text.replace('ООО\xa0', '')

        # далее используется метод contents для того чтобы раскрыть дочерние элементы
        city = vacancy.find('div', class_='vacancy-serp-item__info').contents[1].contents[0]

        json_row = {
            'Ссылка на вакансию': link,
            'Зарплата': salary,
            'Название компнии': employer,
            'Город': city
        }

        vacancies_list.append(json_row)

    return vacancies_list

if __name__ == "__main__":

    parsed_vacancies = parse_hh()

    with open('vacancys.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_vacancies, f, ensure_ascii=False, indent=5)