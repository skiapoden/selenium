#!/usr/bin/env python3

from selenium import webdriver
from firstlink import get_first_article_link

# TODO: config in xml
TARGET = "https://de.wikipedia.org/wiki/Philosophie"
PREFIX_DE = "https://de.wikipedia.org/wiki/"
MAX_HOPS = 20
FILE_NAME = "links.txt"

driver = webdriver.Chrome()

# read input file file
terms = [line.rstrip('\n') for line in open(FILE_NAME)]

print("##########################################################")
print("#                  Tantum optimus testis                 #")
print("##########################################################\n")

f = open("results.csv","w+")

for term in terms:

    hops = 0
    url = PREFIX_DE + term
    while True:

        driver.get(url)

        if url == TARGET:
            # print("SIEG mit {} Hüpfern!".format(hops))
            break

        if hops > MAX_HOPS:
            # print("Ihr hop-Guthaben ist aufgebraucht!")
            hops = 'X'
            break
        try:
            url = get_first_article_link(url)
        except Exception as ex:
            # print(ex)
            hops = 'E'
            break

        hops += 1

        # print(">>> {}. hop ({})".format(hops, url))
    
    # TODO write to file 
    print(">>> {}, {}".format(term, hops))
    f.write("{}, {}\n".format(term, hops))
    
    
print("\nAlea iacta est.")
f.close()
driver.quit()
# domi.getRect()