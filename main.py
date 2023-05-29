import time
from bs4 import BeautifulSoup
from random import randint
import cloudscraper
import json
import csv

with open('config.json', encoding="utf8") as f:
    config = json.loads(f.read())
scanners = config["scanners"].split(", ")

header = ["wallet"]
proxy_list = []
with open('proxy.txt', 'r') as f:
    proxy_list = f.read().splitlines()

wallets = []
with open('wallets.txt', 'r') as f:
    wallets = f.read().splitlines()

scraper = cloudscraper.create_scraper()

with open('goods.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows([header + scanners])

result = []

def check_balance(wallet, scanner):
    balance = None
    for attempt in range(5):
        try:
            proxy_index = randint(0, len(proxy_list) - 1)
            url = f"https://{scanner}/address/{wallet}"
            proxies = {
                "http": f"http://{proxy_list[proxy_index]}",
                "https": f"http://{proxy_list[proxy_index]}",
            }
            time.sleep(config["deelay"])
            parsed_page = scraper.get(url, proxies=proxies, timeout=15).text
            soup = BeautifulSoup(parsed_page, "html.parser")
            body = soup.find('div', class_='card-body')
            balance = body.find('div', class_='col-md-8').text.replace("\n", "")
            print(f'Wallet: {wallet} Balance: {balance} Scanner: {scanner}')
            with open('Goods.txt', 'a') as f:
                f.write(f'Wallet: {wallet} Balance: {balance} Scanner: {scanner} \n')
            break
        except Exception as e:
            print(e)
            with open('failed.txt', 'a') as f:
                f.write(f'{wallet} Scanner: {scanner} \n')
    return balance


for wallet in wallets:
    result = [wallet]
    for scanner in scanners:
       balance = check_balance(wallet, scanner)
       result.append(balance)
    with open('goods.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([result])
