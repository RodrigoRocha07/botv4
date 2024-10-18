from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Configurar o caminho do ChromeDriver
service = Service('bot-2/chromedriver.exe')  # Use barras normais
driver = webdriver.Chrome(service=service)

# Abrir uma página da web
driver.get('https://google.com')

# Esperar alguns segundos
time.sleep(5)

# Encontrar um elemento na página (exemplo: título)
titulo = driver.find_element(By.TAG_NAME, 'h1')
print(titulo.text)

# Fechar o navegador
driver.quit()
