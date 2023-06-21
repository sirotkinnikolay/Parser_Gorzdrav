import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


driver = Chrome()
driver.get("https://gorzdrav.spb.ru/service-free-schedule")
time.sleep(2)
buttons = driver.find_elements(By.XPATH, '/html/body/div/div[1]/div[12]/div[3]/div[1]/div[2]/div[1]/div/div[1]/ul/li')
for number in range(len(buttons)):
    print(number + 1, '-',  buttons[number].text)
district = int(input('Введите ваш район:'))
print(buttons[district - 1].text)
buttons[district - 1].click()
time.sleep(5)
