# uvicorn poapg:app --host 0.0.0.0 --port 8000 


import random
import string
import time
import subprocess
import requests
from fastapi import FastAPI, Path
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


app = FastAPI()

# Listas de nomes e sobrenomes
nomes = [
    "ana", "bia", "bruna", "carla", "cassia", "celso", "clara", "celia", "dani", "denis", 
    "davi", "duda", "eder", "elias", "eliza", "elo", "enzo", "ester", "fabio", "fabia", 
    "fatima", "felipe", "flora", "geisa", "gilda", "gisel", "giuli", "gloria", "graca", "guido", 
    "helio", "igor", "ines", "irina", "isaac", "italo", "jaime", "jana", "jane", "jessy", 
    "joao", "jose", "julia", "julio", "katia", "kezia", "laila", "lais", "laura", "lazaro", 
    "leo", "lia", "lilia", "livia", "lucio", "lucia", "luiza", "lucca", "luna", "maira", 
    "mario", "marta", "maru", "mayra", "mel", "milena", "murilo", "nata", "neli", "neto", 
    "nilda", "nilo", "nina", "noe", "olga", "otavio", "oziel", "pablo", "paulo", "pedro", 
    "pietra", "piera", "raysa", "rebeca", "regia", "rejane", "reni", "rildo"
]

sobrenomes = [
    "abreu", "alves", "amorim", "anjos", "araujo", "assis", "bahia", "barros", "bessa", "braga", 
    "brito", "bueno", "buarque", "caldas", "campos", "cantu", "cardo", "castro", "cezar", "chagas", 
    "coelho", "costa", "couto", "cruz", "cunha", "dias", "duarte", "duran", "dutra", "elias", 
    "farias", "ferro", "fiuza", "flores", "fonseca", "freitas", "furtado", "gama", "garcia", "gato", 
    "gomes", "gouveia", "guedes", "guerra", "gusmao", "jaco", "junque", "lacerda", "lago", "lara", 
    "leite", "lima", "lins", "lopes", "louro", "luz", "macedo", "machado", "madure", "maia", 
    "malta", "manso", "mario", "mello", "melo", "mendes", "menino", "meurer", "mies", "miguez", 
    "mira", "miriam", "molina", "monaco", "monte", "moraes", "moreira", "moura", "muniz", "nabuco", 
    "nader", "naves", "neto", "neves", "nobrega", "noguei", "nunes", "oneto", "paiva", "pardo", 
    "parre", "pedro", "peres", "pimenta", "pinto", "pires", "prado", "preto", "prieto", "prosper", 
    "queiro", "ramos", "rangel", "reis", "rego", "rios", "rocha", "rosas", "salles", "santos", 
    "saro", "saraiva", "silva", "soares", "souza", "spinola", "telles", "terra", "tovar", "trindade", 
    "valada", "vale", "valente", "varela", "vargas", "viana", "vieira", "villa", "vivas", "xavier", 
    "zabini", "zanon", "zarate", "zardo"
]

bot_token = "7222744878:AAFnmmdXpD9ZuhW5LxDteOL02cKociQwtWk"
# chat_id = "-4225954953"

def generate_random_username(nomes, sobrenomes):
    while True:
        nome = random.choice(nomes)
        sobrenome = random.choice(sobrenomes)
        username = nome + sobrenome
        
        if len(username) <= 13:
            numero = str(random.randint(0, 9))
            posicao = random.randint(1, len(username))
            username_com_numero = username[:posicao] + numero + username[posicao:]
            return username_com_numero
        
def generate_random_name(nomes, sobrenomes):
    while True:
        nome = random.choice(nomes)
        sobrenome = random.choice(sobrenomes)
        username = nome +' '+ sobrenome
        
        return username

def send_telegram_msg(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=data)
    return response.json()

def get_current_proxy():
    with open('./chrome_proxy_extension/current_proxy.json', 'r') as file:
        proxy_data = json.load(file)
    return proxy_data

def run_script(url, chat_id):
    subprocess.run(["node", "getRandomProxy.js"])

    current_proxy = get_current_proxy()

    chrome_options = Options()
    chrome_options.add_argument("--load-extension=./chrome_proxy_extension")

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        form = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//form')))
        time.sleep(1)
        random_name = generate_random_name(nomes, sobrenomes)
        random_username = generate_random_username(nomes, sobrenomes)
        time.sleep(4)

        driver.find_element(By.XPATH, '//*[@id="accountRegisterModal"]/form/div[2]/div/div/div/div/input').send_keys(random_username)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Inserir Senha']"))).send_keys('senha741')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Por favor, confirme sua senha novamente']"))).send_keys('senha741')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Preencha o nome verdadeiro e torne -o conveniente para a retirada posterior!']"))).send_keys(random_name) 
        driver.find_element(By.CLASS_NAME, 'van-button').click()

        message = "Dados de Acesso:"
        send_telegram_msg(bot_token, chat_id, message)

        message1 = f"Login: {random_username}\nSenha: senha741"
        send_telegram_msg(bot_token, chat_id, message1)

        message2 = f"{current_proxy['host']}:{current_proxy['port']}:{current_proxy['username']}:{current_proxy['password']}"
        send_telegram_msg(bot_token, chat_id, message2)

        message3 = "=================="
        send_telegram_msg(bot_token, chat_id, message3)



    finally:
        driver.quit()

@app.get("/rodar/{num_interactions}/{nome_url}")
def rodar(num_interactions: int = Path(..., description="Número de interações a serem realizadas"), nome_url: str = Path(..., description="Nome da URL a ser utilizada")):
    
    urls = {
        
        "italo": {
            "url": "https://betsalfa.vip/?id=510015589&type=1&currency=BRL",

            "chat_id": "-4217070412"
        }

    }

    if nome_url not in urls:
        return {"error": "Nome da URL inválido. Use 'dara', 'italo' ou 'kely'."}
    
    url_to_load = urls[nome_url]["url"]
    specific_chat_id = urls[nome_url]["chat_id"]

    send_telegram_msg(bot_token, specific_chat_id, f'✅✅✅✅✅✅✅✅✅✅✅\n\nIniciando envio de \n {num_interactions} CONTAS...\n\n✅✅✅✅✅✅✅✅✅✅✅')

    for i in range(num_interactions):
        try:
            run_script(url_to_load, specific_chat_id)
        except Exception as e:
            print(f"Error encountered during execution {i + 1}: {e}")
            print("Retrying...")

    return {"message": f"{num_interactions} interações foram realizadas com sucesso usando {url_to_load}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
