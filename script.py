import re
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

n = '\n'
user = {"user_district": 1, "user_clinic": 1, "user_doctor_specification": 8, "user_doctor": 1}


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
# driver = Chrome() # обычный браузер
driver.maximize_window()
driver.implicitly_wait(20)
driver.get("https://gorzdrav.spb.ru/service-free-schedule")

"""Выбор района и нажатие на кнопку"""
district_buttons = driver.find_elements(By.XPATH, '/html/body/div/div[1]/div[12]/div[3]/div[1]/div[2]/div[1]/div/div['
                                                  '1]/ul/li')
if user["user_district"] is None:
    for dist_number in range(len(district_buttons)):
        print(f"{dist_number + 1} - {district_buttons[dist_number].text}")
    district = get_user_input(district_buttons)
    print(f" Выбран район: {district_buttons[district - 1].text}")
else:
    district = user["user_district"]
district_buttons[district - 1].click()

# #################################################### CLINIC
clinic_list = driver.find_elements(By.XPATH, '//*[@id="serviceMoOutput"]/div')
list_output(clinic_list)
clinic = get_user_input(clinic_list)
choice_output("Выбрана поликлиника", clinic_list, clinic)
clinic_button = driver.find_elements(By.XPATH, '//*[@id="serviceMoOutput"]/div/button')
clinic_button[clinic - 1].click()

# ##################################################### SPECIFICATION
"""Выбор специализации и нажитие на кнопку"""
doctor_list_specifications = driver.find_elements(By.XPATH, '//*[@id="specialitiesOutput"]/div')
list_output(doctor_list_specifications)
doctor = get_user_input(doctor_list_specifications)
choice_output("Выбрана специализация", doctor_list_specifications, doctor)
doctor_button = driver.find_elements(By.XPATH, '//*[@id="specialitiesOutput"]/div/button')
doctor_button[doctor - 1].click()

# ##################################################### DOCTOR
"""вывод списка врачей"""
doctor_list = driver.find_elements(By.XPATH, '//*[@id="doctorsOutput"]/div')
list_output(doctor_list)
doctor = get_user_input(doctor_list)
choice_output("Выбран врач", doctor_list, doctor)
doctor_two_button = driver.find_elements(By.XPATH, '//*[@id="doctorsOutput"]/div/div[1]/div[2]/div[2]')
doctor_two_button[doctor - 1].click()

# ##################################################### FREE_TIME
"""Получение номера контейнера в котором хранится свободное время для записи"""
###################################################################################################################
# ЕСЛИ НЕТ ТАЛОНОВ ВООБЩЕ, ЗДЕСЬ ВОЗНКАЕТ ОШИБКА, ЕЕ НАДО ОТЛОВИТЬ
free_time_container = driver.find_element(By.XPATH, '//*[@id="doctorsOutput"]/div/div[2]/div/div[2]/div[1]/ul/div')
per = free_time_container.get_attribute('id')

"""Выбор первого свободного времени в списке и нажатие на него"""

def timer(driver_cr, per_cr):
    try:
        free_time_button = driver_cr.find_elements(By.XPATH, f'//*[@id="{per_cr}_container"]/li')
        return free_time_button
    except:
        driver_cr.refresh()
        print("reload")
        timer(driver_cr, per_cr)


timer(driver, per)[0].click()
#############################################################################################################

"""Нажатие на кнопку ЗАПИСАТЬСЯ"""
sign_up_button = driver.find_element(By.XPATH,
                                     f'//*[@id="doctorsOutput"]/div[{doctor}]/div[2]/div/div[2]/div[2]/button')
sign_up_button.click()

"""Форма для заполнения"""
wait = WebDriverWait(driver, 10)
patient_form = wait.until(
    EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="checkPatientForm"]/div[2]/div/span')))
for one_form_line in patient_form:
    print('=====================')
    print(one_form_line.text)

"""Вывод информации о записи пациента"""
info = driver.find_element(By.XPATH, '/html/body/div/div[1]/div[12]/div[2]')
for inf in info.text.splitlines():
    if re.search('Выбрать', inf) is None:
        print(inf)

time.sleep(30)
