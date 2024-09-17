from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager    # Импорт менеджера webdriver.
from selenium.webdriver.chrome.service import Service as ChromeService  # Установка, открытие, закрытие драйвера.
from selenium.webdriver.common.by import By
   
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import time

#--------------------------------------------------------------------

# Инициализация драйвера
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f'user_agent={useragent.random}')

driver.maximize_window()  # Опционально, чтобы максимизировать окно браузера.

HOST = 'https://hh.ru'
URL = 'https://hh.ru/employers_list?query=&hhtmFrom=employers_list&areaId=113&vacanciesNotRequired=True'

driver.get(URL)

wait = WebDriverWait(driver, 10)

#--------------------------------------------------------------------
def Page_URL():
    '''Функция перехода на следующую страницу'''
    try:
        BUTTON_FORWARD = (By.XPATH, "//a[@class='bloko-button']/span[text()='дальше']")

        wait.until(EC.element_to_be_clickable(BUTTON_FORWARD))
        button_forward = driver.find_element(*BUTTON_FORWARD)
        driver.execute_script("arguments[0].click();", button_forward)

        url = driver.current_url  # — возвращает URL документа.
        print(f'URL полученной страницы: {url}')
        return url

    except TimeoutException:
        print('Кнопка "дальше" не найдена (TimeoutException)')
        return None
#--------------------------------------------------------------------
def Link_companies(URL):
    '''Функция открывает страницу и парсит все названия и ссылки компаний на данной странице'''
    try:
        driver.get(URL)

        COMPANIES = (By.XPATH, "//div[@class='item--b0t3EvNeNvRI13OgUyeZ']")
        # COMPANIES = (By.XPATH, "//div[@class='item--M8c5L2cxia1xqTMmWUFN']")

        wait.until(EC.presence_of_all_elements_located(COMPANIES))

        companies = driver.find_elements(*COMPANIES)
        print('------------------------------------------------')
        print(f'Количество компаний на странице: {len(companies)}')

        results = []  # Список для хранения результатов

        for company in companies:
            name_company = company.text
            link_company = company.find_element(By.XPATH, ".//a").get_attribute('href')
            results.append((name_company, link_company))
        return results

    except TimeoutException:
        print('Элементы компаний не найдены на странице (TimeoutException)')
    except Exception as ex:
        print(f"Произошла ошибка: {ex}")
#--------------------------------------------------------------------
def Save_file(results):
    csv_filename = "companies1.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
        # Создаем объект writer
        csv_writer = csv.writer(file)

        # Записываем заголовки (если нужно)
        csv_writer.writerow(["Название компании", "Ссылка на компанию"])
        # Записываем результаты в файл
        for name_company, link_company in results:
            csv_writer.writerow([name_company, link_company])
#---------------------------------------------------------------------
def Start_function():
    try: 
        while True:
            # Сначала обрабатываем компании на текущей странице
            results = Link_companies(driver.current_url)
            Save_file(results)

            # Затем переходим на следующую страницу
            current_url = Page_URL()
            if current_url is None:
                print("Цикл завершен: кнопка 'дальше' не найдена.")
                break  # Выход из цикла, если кнопка "дальше" не найдена

    finally:
        driver.quit()
#--------------------------------------------------------------------

Start_function()


