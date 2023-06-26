import re
import time
from selenium.common import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import datetime

n = '\n'


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


"""Безголовый браузер"""
chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(20)
driver.get("https://gorzdrav.spb.ru/service-free-schedule")

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


time.sleep(5)
timer(driver)[0].click()


def sign_up_button_function(driver_but):
    """Нажатие на кнопку ЗАПИСАТЬСЯ"""
    try:
        sign_up_button = driver_but.find_element(By.XPATH,
                                                 f'//*[@id="doctorsOutput"]/div[{doctor}]/div[2]/div/div[2]/div['
                                                 f'2]/button')
        sign_up_button.click()
    except ElementClickInterceptedException:
        print("ошибка кнопки ЗАПИСЬ")
        driver_but.refresh()
        sign_up_button_function(driver_but)


sign_up_button_function(driver)

# ################################# ДАННЫЕ ПОЛЬЗОВАТЕЛЯ ####################################
user_born = '05.10.1986'
user_data = ['Иванов', 'Владимир', 'Петрович', None, 'test_user@mail.ru', '+79097863245']
# ##########################################################################################

"""Заполнение формы данными пользователя"""
wait = WebDriverWait(driver, 10)
patient_form = wait.until(
    EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="checkPatientForm"]/div[2]/div/span')))

for form_number, user_text in zip(range(1, 7), user_data):
    if form_number == 4:
        continue
    driver.find_element(By.XPATH, f'//*[@id="checkPatientForm"]/div[2]/div[{form_number}]/input').send_keys(
        user_text)

driver.find_element(By.XPATH, '//*[@id="checkPatientForm"]/div[2]/div[4]/div/input').send_keys(user_born)
approval_button = driver.find_element(By.XPATH, '//*[@id="checkPatientForm"]/div[3]/label/input')
approval_button.click()
total_send_button = driver.find_element(By.XPATH, '//*[@id="checkPatientForm"]/div[3]/button')
total_send_button.click()
# Проверка ответа сервера о записи
time.sleep(20)


