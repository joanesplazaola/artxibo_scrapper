import tqdm
from multiprocessing import Pool
import numpy as np
from helpers import get_last_number, get_row, tratatu_datuak

hasiera = get_last_number(["bautizo", "hileta", "ezkontza"])
denera = 1500
zati_kop = 10

jasotzeko = denera - hasiera
zatiak = [1]
zatiak += [int(jasotzeko / zati_kop)] * zati_kop

if jasotzeko % zati_kop != 0:
    zatiak += [jasotzeko % zati_kop]
zatiak = np.cumsum(zatiak)

for index in tqdm.tqdm(range(len(zatiak) - 1)):
    with Pool(50) as p:
        ids = list(range(zatiak[index] + hasiera, zatiak[index + 1] + hasiera))
        records = p.map(get_row, ids)
        tratatu_datuak(records)
