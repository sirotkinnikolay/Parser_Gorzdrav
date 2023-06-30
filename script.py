from function import *
import time
from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging


logging.basicConfig(level=logging.ERROR, filename="log_file.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


def script():
    try:
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
        district_buttons = driver.find_elements(By.XPATH,
                                                '/html/body/div/div[1]/div[12]/div[3]/div[1]/div[2]/div[1]/div/div['
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

        """Вывод списка врачей"""
        doctor_list = driver.find_elements(By.XPATH, '//*[@id="doctorsOutput"]/div')
        list_output(doctor_list)
        doctor = get_user_input(doctor_list)
        choice_output("Выбран врач: ", doctor_list, doctor)
        doctor_two_button = driver.find_elements(By.XPATH, '//*[@id="doctorsOutput"]/div/div[1]/div[2]/div[2]')
        doctor_two_button[doctor - 1].click()
        time.sleep(2)

        timer(driver)[0].click()

        sign_up_button_function(driver, doctor)

        """Заполнение формы данными пользователя"""
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="checkPatientForm"]/div[2]/div/span')))

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
            approval_button_complete = driver.find_element(By.XPATH, '//html/body/div/div[1]/div[12]/div[3]/div['
                                                                     '7]/div/div[3]/label/input')
            approval_button_complete.click()
            total_send_button_complete = driver.find_element(By.XPATH,
                                                             '//html/body/div/div[1]/div[12]/div[3]/div[7]/div/div['
                                                             '5]/div[1]/button[1]')
            total_send_button_complete.click()
            print('Вы записаны ко врачу, проверьте ваш личный кабинет.')
            input('Нажмите ENTER для выхода')

        except ElementNotInteractableException:
            print("Мы не нашли Вашу карточку в выбранной медорганизации. Проверьте корректность введенных данных.")
            input('Нажмите ENTER для выхода')

    except BaseException as err:
        print("Произошла ошибка, попробуйте еще раз.")
        logging.error(err, exc_info=True)
        script()


if __name__ == '__main__':
    script()
