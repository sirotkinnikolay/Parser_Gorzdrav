import time
from selenium.common import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

n = '\n'
user_data = []


def get_user_input(driver_data):
    while True:
        try:
            user_input = int(input("Введите выбранный номер: "))
            if user_input in range(0, len(driver_data) + 1):
                return user_input
            print("ОШИБКА ввода")
        except ValueError:
            print("ОШИБКА ввода")


def list_output(search_data):
    for number in range(len(search_data)):
        print(f"{number + 1} - {search_data[number].text.split(n, 1)[0]}")


def choice_output(text, search_element, element):
    print(f" {text}: {search_element[element - 1].text.split(n, 1)[0]}")


def match(text, alphabet=None):
    if alphabet is None:
        alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return not alphabet.isdisjoint(text.lower())


def user_data_input():
    user_data_text = ['Фамилия(Иванов):', 'Имя(Иван):', 'Отчество(Иванович):',
                      'Дата рождения(30.12.1998):', 'Email(test@mail.ru):', 'Телефон(+79994455)']
    for count, text in zip(range(1, 7), user_data_text):
        one = str(input(text))
        if not match(one) and count <= 3:
            print('Ввод на русском')
            user_data.clear()
            user_data_input()
        user_data.append(one)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", one) and count == 5:
            print("Неправильно введена почта")
            user_data.clear()
            user_data_input()
        user_data.append(one)
        if not re.match(r"ВВЕСТИ ПРОВЕРКУ ФОРМАТА ДАТЫ РОЖДЕНИЯ", one) and count == 4: #####################
            print("Неправильно введена дата рождения")
            user_data.clear()
            user_data_input()
        user_data.append(one)
        if not re.match(r"ВВЕСТИ ПРОВЕРКУ ФОРМАТА ТЕЛЕФОННОГО НОМЕРА", one) and count == 6: #####################
            print("Неправильно введен телефон")
            user_data.clear()
            user_data_input()
        user_data.append(one)

    print(user_data)



"""Безголовый браузер"""
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(20)
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
choice_output("Выбрана поликлиника", clinic_list, clinic)
clinic_button = driver.find_elements(By.XPATH, '//*[@id="serviceMoOutput"]/div/button')
clinic_button[clinic - 1].click()

"""Выбор специализации и нажитие на кнопку"""
doctor_list_specifications = driver.find_elements(By.XPATH, '//*[@id="specialitiesOutput"]/div')
list_output(doctor_list_specifications)
doctor = get_user_input(doctor_list_specifications)
choice_output("Выбрана специализация", doctor_list_specifications, doctor)
doctor_button = driver.find_elements(By.XPATH, '//*[@id="specialitiesOutput"]/div/button')
doctor_button[doctor - 1].click()

"""вывод списка врачей"""
doctor_list = driver.find_elements(By.XPATH, '//*[@id="doctorsOutput"]/div')
list_output(doctor_list)
doctor = get_user_input(doctor_list)
choice_output("Выбран врач", doctor_list, doctor)
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

if driver.find_elements(By.XPATH, '//*[@id="error-modal"]'):
    print("Ваши  личные данные введены неверно.")
else:
    print('Вы записаны ко врачу, проверьте ваш личный кабинет.')

time.sleep(20)
