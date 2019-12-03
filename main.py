import csv
import requests
from bs4 import BeautifulSoup
import tqdm

from helpers import get_last_number

hasiera = get_last_number(["bautizo", "hileta", "ezkontza"])
denera = 1_954_537

bautizo_file = open("bautizo.csv", "a")
b_writter = csv.writer(bautizo_file, delimiter='|', quoting=csv.QUOTE_MINIMAL)
hileta_file = open("hileta.csv", "a")
d_writter = csv.writer(hileta_file, delimiter='|', quoting=csv.QUOTE_MINIMAL)
ezkontza_file = open("ezkontza.csv", "a")
m_writter = csv.writer(ezkontza_file, delimiter='|', quoting=csv.QUOTE_MINIMAL)

values = {"b": b_writter, "d": d_writter, "m": m_writter}

for id in tqdm.tqdm(range(hasiera, denera + 1)):
    orrialdea = f"https://artxiboa.mendezmende.org/es/busque-partidas-sacramentales/ver.html?id={id}&sacramento="
    for k, v in values.items():
        page = requests.get(url=orrialdea + k)
        if page.status_code != 404:
            fitxategia = v
            break

    content = page.content
    soup = BeautifulSoup(content, 'html.parser')

    taula = soup.find('section', id='identificacion')

    ident = [td.get_text() for td in taula.find_all('td')]

    taula2 = soup.find('section', id='localizacion')
    loc = [td.get_text() for td in taula2.find_all('td')]

    fitxategia.writerow([id] + ident + loc)
