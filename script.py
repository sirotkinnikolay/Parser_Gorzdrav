import time
from selenium.common import NoSuchElementException, ElementClickInterceptedException, TimeoutException,\
    ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

n = '\n'
user_data = []


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
    if not re.match(regular, user_info):
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
            user_info_input(r"\d\d[.]\d\d[.]\d{4}", text)
        if count == 5:
            user_info_input(r"[^@]+@[^@]+\.[^@]+", text)
        if count == 6:
            user_info_input(r"[+]\d{11}", text)
    return


"""'Безголовый' браузер"""
chrome_options = Options()
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(10)
driver.get("https://gorzdrav.spb.ru/service-free-schedule")

user_data_input()

"""Выбор района и нажатие на кнопку"""
district_buttons = driver.find_elements(By.XPATH, '/html/body/div/div[1]/div[12]/div[3]/div[1]/div[2]/div[1]/div/div['
                                                  '1]/ul/li')
for dist_number in range(len(district_buttons)):
    print(f"{dist_number + 1} - {district_buttons[dist_number].text}")
district = get_user_input(district_buttons)
print(f" Выбран район: {district_buttons[district - 1].text}")
district_buttons[district - 1].click()

"""Выбор поликлиники и нажатие на кнопку"""
clinic_list = driver.find_elements(By.XPATH, '//*[@id="serviceMoOutput"]/div')
list_output(clinic_list)
clinic = get_user_input(clinic_list)
choice_output("Выбрана поликлиника: ", clinic_list, clinic)
clinic_button = driver.find_elements(By.XPATH, '//*[@id="serviceMoOutput"]/div/button')
clinic_button[clinic - 1].click()

"""Выбор специализации и нажитие на кнопку"""
doctor_list_specifications = driver.find_elements(By.XPATH, '//*[@id="specialitiesOutput"]/div')
list_output(doctor_list_specifications)
doctor = get_user_input(doctor_list_specifications)
choice_output("Выбрана специализация: ", doctor_list_specifications, doctor)
doctor_button = driver.find_elements(By.XPATH, '//*[@id="specialitiesOutput"]/div/button')
doctor_button[doctor - 1].click()

"""вывод списка врачей"""
doctor_list = driver.find_elements(By.XPATH, '//*[@id="doctorsOutput"]/div')
list_output(doctor_list)
doctor = get_user_input(doctor_list)
choice_output("Выбран врач: ", doctor_list, doctor)
doctor_two_button = driver.find_elements(By.XPATH, '//*[@id="doctorsOutput"]/div/div[1]/div[2]/div[2]')
doctor_two_button[doctor - 1].click()


def timer(driver_cr):
    """Выбор первого свободного времени в списке и нажатие на него"""
    try:
        """Получение номера контейнера в котором хранится свободное время для записи"""
        free_time_container = driver.find_element(By.XPATH,
                                                  '//*[@id="doctorsOutput"]/div/div[2]/div/div[2]/div[1]/ul/div')
        per = free_time_container.get_attribute('id')
        free_time_button = driver_cr.find_elements(By.XPATH, f'//*[@id="{per}_container"]/li')
        return free_time_button
    except NoSuchElementException:
        driver_cr.refresh()
        print("Свободных талонов нет, идет ожидание.")
        timer(driver_cr)


time.sleep(2)
timer(driver)[0].click()


def sign_up_button_function(driver_but):
    """Нажатие на кнопку ЗАПИСАТЬСЯ"""
    try:
        sign_up_button = driver_but.find_element(By.XPATH,
                                                 f'//*[@id="doctorsOutput"]/div[{doctor}]/div[2]/div/div[2]/div['
                                                 f'2]/button')
        sign_up_button.click()
    except ElementClickInterceptedException:
        driver_but.refresh()
        sign_up_button_function(driver_but)


sign_up_button_function(driver)

"""Заполнение формы данными пользователя"""
wait = WebDriverWait(driver, 10)
patient_form = wait.until(
    EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="checkPatientForm"]/div[2]/div/span')))

for form_number, user_text in zip(range(1, 7), user_data):
    if form_number == 4:
        driver.find_element(By.XPATH, '//*[@id="checkPatientForm"]/div[2]/div[4]/div/input').send_keys(
            user_data[form_number - 1])
        continue
    driver.find_element(By.XPATH, f'//*[@id="checkPatientForm"]/div[2]/div[{form_number}]/input').send_keys(
        user_text)

approval_button = driver.find_element(By.XPATH, '//*[@id="checkPatientForm"]/div[3]/label/input')
approval_button.click()
total_send_button = driver.find_element(By.XPATH, '//*[@id="checkPatientForm"]/div[3]/button')
total_send_button.click()

try:
    approval_button_complete = driver.find_element(By.XPATH, '//html/body/div/div[1]/div[12]/div[3]/div[7]/div/div['
                                                             '3]/label/input')
    approval_button_complete.click()
    total_send_button_complete = driver.find_element(By.XPATH, '//html/body/div/div[1]/div[12]/div[3]/div[7]/div/div['
                                                               '5]/div[1]/button[1]')
    total_send_button_complete.click()
    print('Вы записаны ко врачу, проверьте ваш личный кабинет.')
    print("Для выхода из программы нажмите CTRL + C")

except ElementNotInteractableException:
    print("Мы не нашли Вашу карточку в выбранной медорганизации. Проверьте корректность введенных данных.")
    print("Для выхода из программы нажмите CTRL + C")

time.sleep(20)
