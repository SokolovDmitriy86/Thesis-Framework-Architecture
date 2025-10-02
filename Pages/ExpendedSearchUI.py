import re
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class Search:

    def __init__(self, driver):
        with allure.step('Открыть сайт "Кинопоиск"'):
            self._driver = driver
            self._driver.get('https://www.kinopoisk.ru/')

        with allure.step('Закрыть pop-up'):
            try:
                popup_close_button = WebDriverWait(self._driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                         '/html/body'
                         '/div[5]/div/div/div/div[1]/div[2]/button[2]')))
                popup_close_button.click()
            except TimeoutException:
                print("Pop-up не появился или не был найден.")

        with allure.step('Развернуть окно в полноэкранный режим'):
            self._driver.maximize_window()
        self._driver.implicitly_wait(10)

    def _open_extended_search(self):
        with allure.step('Кликнуть на кнопку расширенного поиска'):
            self._driver.find_element(
                By.XPATH, "//a[@aria-label='Расширенный поиск']").click()

    def _click_search_button(self):
        with allure.step('Кликнуть кнопку поиска'):
            WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "//input[@class='el_18 submit nice_button']"))).click()

    def _extract_search_results_count(self):
        try:  # Добавляем обработку исключений
            element = self._driver.find_element(
                By.CLASS_NAME, 'search_results_topText')
            text = element.text.strip()
            match = re.search(r'\d+', text)  # Ищем число в тексте
            if match:
                return int(match.group(0))  # Возвращаем число как int
            else:
                print(
                    f"Не удалось извлечь количество результатов из текста:"
                    f" {text}")
                return 0  # Возвращаем 0, если не удалось найти число
        except Exception as e:
            print(f"Ошибка при извлечении количества результатов: {e}")
            return 0  # Возвращаем 0 в случае ошибки

    @allure.title('UI. Расширенный поиск по названию фильма')
    def search_by_name(self):
        self._open_extended_search()

        with allure.step('Ввести в поле "Искать фильм:" название фильма'):
            self._driver.find_element(
                By.ID, 'find_film').send_keys('John Wick')

        self._click_search_button()

        return self._extract_search_results_count()

    @allure.title('UI. Расширенный поиск по году выхода фильма')
    def search_by_year(self):
        self._open_extended_search()

        with allure.step('Ввести в поле "+ год:" год выхода фильма'):
            self._driver.find_element(By.ID, 'year').send_keys('1996')

        self._click_search_button()

        return self._extract_search_results_count()

    @allure.title('UI. Расширенный поиск по стране')
    def search_by_country(self):
        self._open_extended_search()

        with allure.step('Выбрать страну в выпадающем списке "+ страна:"'):
            self._driver.find_element(
                By.ID, 'country').find_element(
                By.XPATH, '//*[@id="country"]/option[43]').click()

        self._click_search_button()

        with allure.step('Получение результатов поиска'):
            xpath_part1 = ('//*[@id="block_left_padtop"]'
                           '/div/table/tbody/tr/td/table/tbody/tr[1]')
            xpath_part2 = '/td/table/tbody/tr[1]/td/h1/font'
            search_by_country_result = self._driver.find_element(
                By.XPATH, (xpath_part1 + xpath_part2)).text
            print(search_by_country_result)
            return str(search_by_country_result)

    @allure.title('UI. Расширенный поиск по жанру фильма')
    def search_by_genre(self):
        self._open_extended_search()

        with allure.step('Выбрать жанр в поле выбора жанра'):
            self._driver.find_element(
                By.XPATH, '//*[@id="m_act[genre]"]/option[7]').click()

        self._click_search_button()

        return self._extract_search_results_count()

    @allure.title('UI. Расширенный поиск по прокатчику')
    def search_by_rental_company(self):
        self._open_extended_search()

        with allure.step(
                'Выбрать прокатчика в выпадающем списке "+ прокатчик:"'):
            self._driver.find_element(
                By.XPATH, '//*[@id="company"]/option[62]').click()

        self._click_search_button()

        return self._extract_search_results_count()
