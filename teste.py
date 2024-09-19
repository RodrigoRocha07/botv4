from main import run_script

urls = {
    
    "italo": {
        "url": "https://betx3.com/?id=337387816&currency=BRL&type=2",

        "chat_id": "-4217070412"
    },
    "kely": {
        "url": "https://betx3.com/?id=659920364&currency=BRL&type=2",
        "chat_id": "-4283310871"
    }

}

url_to_load = urls[nome_url]["url"]
specific_chat_id = urls[nome_url]["chat_id"]

if nome_url not in urls:
    return {"error": "Nome da URL inválido. Use 'dara', 'italo' ou 'kely'."}

run_script()


