import allure
import pytest
from selenium import webdriver
from Pages.ExpendedSearchUI import Search


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture
def search(driver):
    return Search(driver)


@pytest.fixture(scope="function")
def setup(driver):
    """
    Предусловия:
    1. Открыть сайт "Кинопоиск"
    2. Закрыть pop-up (если есть)
    3. Развернуть окно в полноэкранный режим
    """
    driver.get("https://www.kinopoisk.ru/")
    driver.maximize_window()
    yield


@allure.epic('UI. Расширенный поиск фильмов')
@allure.story('UI. Проверка расширенного поиска фильма')
@allure.title('UI. Расширенный поиск по названию фильма')
def test_ui_name(search, setup):
    result_by_name = search.search_by_name()
    print(result_by_name)
    assert result_by_name > 0, (
        f"Ожидалось, что будет найден фильм по названию, "
        f"но результат: {result_by_name}"
    )


@allure.epic('UI. Расширенный поиск фильмов')
@allure.story('UI. Проверка расширенного поиска фильма')
@allure.title('UI. Расширенный поиск по году выхода фильма')
def test_ui_year(search, setup):
    year_count = search.search_by_year()
    with allure.step('Проверка, что поиск по году возвращает результаты'):
        print(year_count)
        assert year_count > 0, (
            f"Ожидалось, что будут найдены фильмы по году, "
            f"но результат: {year_count}"
        )


@allure.epic('UI. Расширенный поиск фильмов')
@allure.story('UI. Проверка расширенного поиска фильма')
@allure.title('UI. Расширенный поиск по стране')
def test_ui_country(search, setup):
    result_by_country = search.search_by_country()
    print(result_by_country)
    try:
        country_count = int(
            result_by_country.strip('()'))  # Преобразуем к числу
        assert country_count > 0, (
            f"Ожидалось, что количество стран будет больше 0, "
            f"но результат: {result_by_country}"
        )
    except ValueError:
        assert False, (
            f"Не удалось преобразовать результат '{result_by_country}' "
            f"в число"
        )


@allure.epic('UI. Расширенный поиск фильмов')
@allure.story('UI. Проверка расширенного поиска фильма')
@allure.title('UI. Расширенный поиск по жанру фильма')
def test_ui_genre(search, setup):
    genre_count = search.search_by_genre()
    with allure.step('Проверка, что поиск по жанру возвращает результаты'):
        print(genre_count)
        assert genre_count > 0, (
            f"Ожидалось, что будут найдены фильмы по жанру, "
            f"но результат: {genre_count}"
        )


@allure.epic('UI. Расширенный поиск фильмов')
@allure.story('UI. Проверка расширенного поиска фильма')
@allure.title('UI. Расширенный поиск по прокатчику')
def test_ui_rental_company(search, setup):
    result_by_rental_company = search.search_by_rental_company()
    print(result_by_rental_company)
    assert result_by_rental_company > 0, (
        f"Ожидалось, что будут найдены фильмы по прокатчику, "
        f"но результат: {result_by_rental_company}"
    )
