from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Загружаем драйвер браузера Chrome
chrome_driver_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
service = Service(chrome_driver_path)
service.start()
driver = webdriver.Remote(service.service_url)

# Открываем веб-страницу
driver.get("https://www.centralcharts.com/en/6573-natural-gas/charts")

# Находим элемент, содержащий график
chart_element = driver.find_element_by_xpath("//div[@class='chart-container']")

# Делаем скриншот только этого элемента
chart_element.screenshot("chart_screenshot.png")

# Закрываем браузер
driver.quit()