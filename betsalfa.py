import random
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
import os
from getRandomProxy import get_random_proxy
app = FastAPI()

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

# Função para gerar um nome de usuário aleatório
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
        
# Função para gerar um nome completo aleatório
def generate_random_name(nomes, sobrenomes):
    while True:
        nome = random.choice(nomes)
        sobrenome = random.choice(sobrenomes)
        username = nome + ' ' + sobrenome
        return username

# Função para enviar mensagens pelo Telegram
def send_telegram_msg(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=data)
    return response.json()

def limpar_arquivo(caminho_arquivo):
    try:
        # Abre o arquivo no modo de escrita 'w', que limpa o conteúdo
        with open(caminho_arquivo, 'w') as arquivo:
            # Não precisa escrever nada, isso já limpa o arquivo
            pass
        print(f"Arquivo {caminho_arquivo} foi limpo com sucesso.")
    except Exception as e:
        print(f"Erro ao limpar o arquivo: {e}")


# Função para obter o proxy atual de um arquivo JSON
#essa funcao n esta sendo usada pois estou pegando a proxy diretamente da funcao getRandomProxy, assim caso ela retorne vazia a funcao para

def get_current_proxy():
    try:
        proxy_path = os.path.join('.', 'chrome_proxy_extension', 'current_proxy.json')
        print(f"Loading proxy file from: {proxy_path}")  # Log do caminho do arquivo
        with open(proxy_path, 'r') as file:
            proxy_data = json.load(file)
            print(f"Proxy data loaded: {proxy_data}")  # Log do conteúdo
            limpar_arquivo(proxy_path)
        return proxy_data
    except FileNotFoundError:
        print(f"Arquivo {proxy_path} não encontrado.")
        return None

# Função para rodar o script
def run_script(url, chat_id):
    try:
        current_proxy = get_random_proxy()
    except FileNotFoundError as e:
        print(f"Erro ao rodar o script: Arquivo não encontrado - {e.filename}")
        return
    except subprocess.CalledProcessError as e:
        print(f"Erro ao rodar o script: {e}")
        return

    if not current_proxy:
        print('')
        print("Proxy não encontrado. Abortando execução.")
        print('')
        return
    else:
        chrome_options = Options()
        chrome_options.add_argument("--load-extension=.\\chrome_proxy_extension")

        try:
            service = Service("chromedriver.exe")
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except FileNotFoundError as e:
            print(f"Erro: Chromedriver não encontrado - {e.filename}")
            return

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
            #driver.find_element(By.CLASS_NAME, 'van-button').click()

            # Enviar mensagens de sucesso via Telegram
            send_telegram_msg(bot_token, chat_id, "Dados de Acesso:")
            send_telegram_msg(bot_token, chat_id, f"Login: {random_username}\nSenha: senha741")
            send_telegram_msg(bot_token, chat_id, f"{current_proxy['host']}:{current_proxy['port']}:{current_proxy['username']}:{current_proxy['password']}")
            send_telegram_msg(bot_token, chat_id, "==================")

        finally:
            driver.quit()

@app.get("/rodar/{num_interactions}/{nome_url}")
def rodar(num_interactions: int = Path(..., description="Número de interações a serem realizadas"), nome_url: str = Path(..., description="Nome da URL a ser utilizada")):

    urls = {
        
        "italo": {
            "url": "https://betsalfa.vip/?id=516307523&type=1&currency=BRL",

            "chat_id": "-4217070412"
        },
        "kely": {
            "url": "https://betsalfa.vip/?id=688137424&type=1&currency=BRL",
            "chat_id": "-4283310871"
        },
        "dara": {
            "url": "https://betsalfa.vip/?id=376121080&type=1&currency=BRL",
            "chat_id": "-4213465625"
        }

    }
    

    if nome_url not in urls:
        return {"error": "Nome da URL inválido. Use 'italo'."}
    
    url_to_load = urls[nome_url]["url"]
    specific_chat_id = urls[nome_url]["chat_id"]

    send_telegram_msg(bot_token, specific_chat_id, f'✅ Iniciando envio de {num_interactions} CONTAS... ✅')

    for i in range(num_interactions):
        try:
            run_script(url_to_load, specific_chat_id)
        except Exception as e:
            print(f"Erro na execução {i + 1}: {e}")
            print("Tentando novamente...")

    return {"message": f"{num_interactions} interações foram realizadas com sucesso usando {url_to_load}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)