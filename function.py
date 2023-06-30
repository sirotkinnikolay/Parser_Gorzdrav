import re
import time

from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By

user_data = []
n = '\n'


def sign_up_button_function(driver_but, doctor_input):
    """Нажатие на кнопку ЗАПИСАТЬСЯ"""
    try:
        sign_up_button = driver_but.find_element(By.XPATH,
                                                 f'//*[@id="doctorsOutput"]/div[{doctor_input}]/div[2]/div/div[2]/div['
                                                 f'2]/button')
        sign_up_button.click()
    except ElementClickInterceptedException:
        driver_but.refresh()
        sign_up_button_function(driver_but, doctor_input)


def timer(driver_cr):
    """Выбор первого свободного времени в списке и нажатие на него"""
    try:
        """Получение номера контейнера в котором хранится свободное время для записи"""
        free_time_container = driver_cr.find_element(By.XPATH,
                                                  '//*[@id="doctorsOutput"]/div/div[2]/div/div[2]/div[1]/ul/div')
        per = free_time_container.get_attribute('id')
        free_time_button = driver_cr.find_elements(By.XPATH, f'//*[@id="{per}_container"]/li')
        return free_time_button
    except NoSuchElementException:
        driver_cr.refresh()
        print("Свободных талонов нет, идет ожидание.")
        time.sleep(10*60)
        timer(driver_cr)


def get_user_input(driver_data):
    """Функция проверки корректного выбора пользователем из списка"""
    while True:
        try:
            user_input = int(input("Введите выбранный номер: "))
            if user_input in range(0, len(driver_data) + 1):
                return user_input
            print("ОШИБКА ввода")
        except ValueError:
            print("ОШИБКА ввода")


def list_output(search_data):
    """Функция вывода списка для выбора"""
    for number in range(len(search_data)):
        print(f"{number + 1} - {search_data[number].text.split(n, 1)[0]}")


def choice_output(text, search_element, element):
    """Функция вывода результата выбора пользователя"""
    print(f" {text}: {search_element[element - 1].text.split(n, 1)[0]}")


def match_letter(text, alphabet=None):
    """Функция проверки ввода русскими буквами"""
    if alphabet is None:
        alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return not alphabet.isdisjoint(text.lower())


def user_info_input(regular, text_func):
    """ Функция проверки ввода данных пользователем """
    user_info = str(input(text_func))
    if not re.fullmatch(regular, user_info):
        print("Неправильный ввод: " + text_func)
        user_info_input(regular, text_func)
    else:
        user_data.append(user_info)


def user_data_input():
    """Функция ввода данных пользователя"""
    user_data_text = ['Фамилия(Иванов):', 'Имя(Иван):', 'Отчество(Иванович):',
                      'Дата рождения(30.12.1998):', 'Email(test@mail.ru):', 'Телефон(+79994445590)']
    for count, text in zip(range(1, 7), user_data_text):
        if count <= 3:
            surname_name_patronymic = str(input(text))
            if not match_letter(surname_name_patronymic) and count <= 3:
                print('Введите русскими буквами.')
                user_data.clear()
                user_data_input()
            user_data.append(surname_name_patronymic)
        if count == 4:
            user_info_input(r"\d\d[.]\d\d[.][1-2][0,9]\d\d", text)
        if count == 5:
            user_info_input(r"[^@]+@[^@]+\.[^@]+", text)
        if count == 6:
            user_info_input(r"[+][7]\d{10}", text)
