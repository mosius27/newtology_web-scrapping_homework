import requests
from bs4 import BeautifulSoup
import json
import scripts.logger as log
log.Logging()

@log.logger.catch()
def get_vacancies(searchLink: str) -> list:

    header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    response = requests.get(searchLink, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    info = soup.find('template', {'id': 'HH-Lux-InitialState'}).text
    items = json.loads(info)
    vacancies = items['vacancySearchResult']['vacancies']

    return vacancies

@log.logger.catch()
def get_vacancy_info(vacancyLink) -> dict:
    
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    response = requests.get(vacancyLink, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    info = soup.find('template', {'id': 'HH-Lux-InitialState'}).text
    items = json.loads(info)
    vacancyItems = items['vacancyView']
    desc = vacancyItems['description'].lower()
    if 'django' not in desc or 'flask' not in desc:
        log.logger.info('В описании отсутстувуют ключевые слова')
        return None

    infoDict = {}
    infoDict['Ссылка'] = vacancyLink

    try:

        try:
            salary = str(vacancyItems['compensation']['from'])
            try:
                salary += f" - {vacancyItems['compensation']['to']}"
            except:
                salary = f"от {salary} {vacancyItems['compensation']['currencyCode']}"
        except:
            salary = f"до {vacancyItems['compensation']['to']} {vacancyItems['compensation']['currencyCode']}"

        infoDict['Вилка зп'] = salary

    except:
        infoDict['Вилка зп'] = 'з/п не указана'

    infoDict['Название компании'] = vacancyItems['company']['name']
    infoDict['Город'] = vacancyItems['area']['name']
    
    return infoDict