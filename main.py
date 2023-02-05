import scripts.hh as hh
import scripts.workingWithJson as workingWithJson
import time
import scripts.logger as log
log.Logging()

if __name__ == "__main__":

    searchLink = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
    log.logger.info('Начало сбора ссылок вакансий...')
    vacancies = hh.get_vacancies(searchLink)
    log.logger.info('Сбор ссылок вакансий завершен...')

    log.logger.info('Начало сбора информации с собранных вакансий...')
    savedVacancy = workingWithJson.read_json('data/vacanciesInfo.json')
    for item in vacancies:
        vacancyId = item['vacancyId']
        url = f'https://hh.ru/vacancy/{vacancyId}'
        log.logger.info(f'Получение данных из вакансии {url}')
        vacancyInfo = hh.get_vacancy_info(url)
        if vacancyInfo:
            savedVacancy[vacancyId] = vacancyInfo
            workingWithJson.write_json(path='data/vacanciesInfo.json', var=savedVacancy)
        time.sleep(1)