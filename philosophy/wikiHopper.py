#!/usr/bin/env python3

import os
import logging as vsklogger
from selenium import webdriver
from firstlink import get_first_article_link

# configure logger
vsklogger.basicConfig(level=vsklogger.ERROR)

# TODO: config in xml
TARGET = "https://de.wikipedia.org/wiki/Philosophie"
PREFIX_DE = "https://de.wikipedia.org/wiki/"
MAX_HOPS = 20
INPUT_FILE_NAME = "links.txt"
INPUT_FILE_NAME = "links.all.txt"
OUTPUT_FILE_NAME = "results.csv"

dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, INPUT_FILE_NAME)
output_file = os.path.join(dirname, OUTPUT_FILE_NAME)

driver = webdriver.Chrome()

# get links
# TODO: this but better
terms = [line.rstrip('\n') for line in open(input_file) if not line.startswith('#') and line.strip()]

print("##########################################################")
print("#                  Tantum optimus testis                 #")
print("##########################################################\n")

f = open(output_file,"w+")

for term in terms:

    hops = 0
    url = PREFIX_DE + term
    while True:

        driver.get(url)

        if url == TARGET:
            vsklogger.debug("SIEG mit {} Hüpfern!".format(hops))
            break

        if hops > MAX_HOPS:
            vsklogger.warning("Ihr hop-Guthaben ist aufgebraucht!")
            hops = 'X'
            break
        try:
            url = get_first_article_link(url)
        except Exception as ex:
            vsklogger.warning(ex)
            hops = 'E'
            break

        hops += 1
        vsklogger.info(">>> {}. hop ({})".format(hops, url))
    
    print(">>> {}, {}".format(term, hops))
    f.write("{}, {}\n".format(term, hops))
    
print("\nAlea iacta est.")
f.close()
driver.quit()
# domi.getRect()