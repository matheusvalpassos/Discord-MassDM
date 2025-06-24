import requests
import time
import json


# Carregar token
def load_token():
    try:
        with open("config/token.json") as f:
            return json.load(f).get("token")
    except Exception as e:
        print(f"[ERRO] Não foi possível carregar o token: {e}")
        exit()


# Cabeçalho global
HEADERS = {
    "Authorization": load_token(),
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
}

# Lista de servidores e seus canais
SERVERS = [
    {
        "guild_id": "1194503218487640084",  # Shaiya PH
        "invite_code": "shaiyaph",
        "channel_ids": [
            "1197427756158427136",  # Global
            "1197091832895639552",  # Pinoy
            "1201175953523621959",  # Non Ph
        ],
    },
    {
        "guild_id": "471155127772905482",  # Community
        "invite_code": "aSKzf43r",
        "channel_ids": [
            "488308934696763402",  # General
            "961232746921984000",  # Discussions
        ],
    },
]


# Ler mensagem do arquivo .txt
def load_custom_message():
    try:
        with open("messages/custom_message.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"[ERRO] Não foi possível carregar a mensagem: {e}")
        return ""


custom_message = load_custom_message()


# Função: Entrar no servidor
def join_guild(invite_code):
    url = f"https://discord.com/api/v10/invites/{invite_code}"
    response = requests.post(url, headers=HEADERS, json={})
    return response.status_code == 200


# Função: Enviar embed para usuário
def send_embed(user_id):
    url = "https://discord.com/api/v10/users/@me/channels"
    data = {"recipient_id": user_id}
    r1 = requests.post(url, headers=HEADERS, json=data)

    if r1.status_code not in [200, 201]:
        return False

    channel = r1.json()
    channel_id = channel["id"]

    embed = {
        "title": "🔥 Shaiya Asgard - The New Adventure!",
        "description": custom_message,
        "color": 15844367,
        "footer": {
            "text": "Enviado por Asgard DM Tools",
        },
        "author": {
            "name": "Shaiya Asgard",
        },
    }

    payload = {"content": "", "embeds": [embed]}

    url2 = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    r2 = requests.post(url2, headers=HEADERS, json=payload)

    return r2.status_code in [200, 201]


# Função: Raspar usuários de múltiplos canais
def scrape_users_from_channels(channel_ids):
    users = set()

    for channel_id in channel_ids:
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit=100"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            continue

        messages = response.json()
        for msg in messages:
            author = msg["author"]
            if not author.get("bot"):
                user_line = (
                    f"{author['id']} - {author['username']}#{author['discriminator']}"
                )
                users.add(user_line)

    return list(users)


# Função: Entrar em todos os servidores
def join_servers(servers):
    for server in servers:
        invite_code = server["invite_code"]
        guild_id = server["guild_id"]

        success = join_guild(invite_code)
        if success:
            print(f"[✓] Entrou no servidor {guild_id}")
        else:
            print(f"[!] Falha ao entrar no servidor {guild_id}")
        time.sleep(5)  # Evita banimento por spam de entradas
