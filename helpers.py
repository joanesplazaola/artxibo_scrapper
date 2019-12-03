import csv
from collections import defaultdict

import requests
from bs4 import BeautifulSoup


def get_last_number(files):
    values = []
    for file in files:
        with open(f'{file}.csv', 'r') as f:
            opened_file = f.readlines()
            if opened_file:
                var = opened_file[-1].split('|')[0]
                values.append(int(var))

    if values:
        init = max(values)
    else:
        init = 0
    return init



def get_row(id):
    values = ["b", "d", "m"]
    orrialdea = f"https://artxiboa.mendezmende.org/es/busque-partidas-sacramentales/ver.html?id={id}&sacramento="
    for v in values:
        page = requests.get(url=orrialdea + v)
        if page.status_code != 404:
            fitxategia = v
            break
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    taula = soup.find('section', id='identificacion')

    ident = [td.get_text() for td in taula.find_all('td')]

    taula2 = soup.find('section', id='localizacion')
    loc = [td.get_text() for td in taula2.find_all('td')]
    return [id] + ident + loc, fitxategia


def tratatu_datuak(records):
    fitxategiak = {"b": "bautizo", "m": "ezkontza", "d": "hileta"}
    d = defaultdict(list)
    types = list(list(zip(*records))[1])
    content = list(list(zip(*records))[0])
    for i, x in enumerate(types):
        d[x].append(content[i])

    for k, v in d.items():
        gorde_fitxategietan(v, fitxategiak[k])


def gorde_fitxategietan(records, fitxategia):
    with open(f"{fitxategia}.csv", "a") as file:
        writer = csv.writer(file, delimiter='|', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        writer.writerows(records)
