import re
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

n = '\n'

driver = Chrome()
driver.implicitly_wait(20)
driver.get("https://gorzdrav.spb.ru/service-free-schedule")

# ################################################## DISTRICT
"""ПОиск и вывод списка районов"""

district_buttons = driver.find_elements(By.XPATH, '/html/body/div/div[1]/div[12]/div[3]/div[1]/div[2]/div[1]/div/div['
                                                 '1]/ul/li')
for dist_number in range(len(district_buttons)):
    print(f"{dist_number + 1} - {district_buttons[dist_number].text}")
"""Выбор района и нажатие на кнопку"""
district = int(input('Выберите район: '))
print(f" Выбран район: {district_buttons[district - 1].text}")
district_buttons[district - 1].click()

# #################################################### CLINIC
clinic_list = driver.find_elements(By.XPATH, '//*[@id="serviceMoOutput"]/div')
for clin_number in range(len(clinic_list)):
    print(f"{clin_number + 1} -{clinic_list[clin_number].text.split(n, 1)[0][8:]}")
clinic = int(input("Выберите поликлинику: "))
print(f"Выбрана поликлиника: {clinic_list[clinic - 1].text.split(n, 1)[0][8:]}")
clinic_button = driver.find_elements(By.XPATH, '//*[@id="serviceMoOutput"]/div/button')
clinic_button[clinic - 1].click()

# ##################################################### SPECIFICATION
"""Поиск и вывод списка специализаций врачей"""
doctor_list = driver.find_elements(By.XPATH, '//*[@id="specialitiesOutput"]/div')
for doc_number in range(len(doctor_list)):
    print(f"{doc_number + 1} - {doctor_list[doc_number].text.split(n, 1)[0]}")

"""Выбор специализации и нажитие на кнопку"""
doctor = int(input("Выберите специализацию: "))
print(f"Выбрана специализация: {doctor_list[doctor - 1].text.split(n, 1)[0]}")
doctor_button = driver.find_elements(By.XPATH, '//*[@id="specialitiesOutput"]/div/button')
doctor_button[doctor - 1].click()

# ##################################################### DOCTOR
"""Поиск и вывод списка врачей"""
doctor_two_list = driver.find_elements(By.XPATH, '//*[@id="doctorsOutput"]/div')
for doc_two_number in range(len(doctor_two_list)):
    print(f"{doc_two_number + 1} - {doctor_two_list[doc_two_number].text.split(n, 1)[0]}")

"""Выбор врача и нажатие на кнопку"""
doctor_two = int(input("Выберите врача: "))
print(f"Выбран врач: {doctor_two_list[doctor_two - 1].text.split(n, 1)[0]}")
doctor_two_button = driver.find_elements(By.XPATH, '//*[@id="doctorsOutput"]/div/div[1]/div[2]/div[2]')
doctor_two_button[doctor_two - 1].click()

# ##################################################### FREE_TIME
"""Получение номера контейнера в котором хранится свободное время для записи"""
free_time = driver.find_element(By.XPATH, '//*[@id="doctorsOutput"]/div/div[2]/div/div[2]/div[1]/ul/div')
per = free_time.get_attribute('id')

"""Выбор первого свободного времени в списке и нажатие на него"""
free_number = driver.find_elements(By.XPATH, f'//*[@id="{per}_container"]/li')
free_number[0].click()

"""Нажатие на кнопку ЗАПИСАТЬСЯ"""
cl_button = driver.find_element(By.XPATH, f'//*[@id="doctorsOutput"]/div[{doctor_two}]/div[2]/div/div[2]/div[2]/button')
cl_button.click()
time.sleep(5)
"""Вывод информации о записи пациента"""
info = driver.find_element(By.XPATH, '/html/body/div/div[1]/div[12]/div[2]')
for inf in info.text.splitlines():
    if re.search('Выбрать', inf) is None:
        print(inf)

"""Форма для заполнения"""
patient_form = driver.find_elements(By.XPATH, '//*[@id="checkPatientForm"]/div[2]/div/span')
for one_form_line in patient_form:
    print('=====================')
    print(one_form_line.text)
time.sleep(30)
