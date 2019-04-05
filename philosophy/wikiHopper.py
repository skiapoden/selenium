#!/usr/bin/env python3

import os
import logging as vsklogger
import selenium.common.exceptions
from selenium.common.exceptions import InvalidArgumentException as Exeption
import xml.etree.ElementTree as ET

from firstlink import get_first_article_link

# configure logger
vsklogger.basicConfig(level=vsklogger.INFO, filename="hopper.log")

# read configuration file
dirname = os.path.dirname(__file__)
config = os.path.join(dirname, "config.xml")
tree = ET.parse(config)
root = tree.getroot()

TARGET = root.findtext("wikiHopper/target")
if root.findtext("wikiHopper/lang") == "DE":
    PREFIX = "https://de.wikipedia.org/wiki/"
else:
    raise Exeption("Illegal language")
if root.find("wikiHopper/advanced-testing").get("value") == "cool":
    INPUT_FILE_NAME = root.findtext("wikiHopper/input-advanced")
else:
    INPUT_FILE_NAME = root.findtext("wikiHopper/input")
OUTPUT_FILE_NAME = root.findtext("wikiHopper/output")
MAX_HOPS = int(root.findtext("wikiHopper/max-hops"))

vsklogger.info("Configuration configured")

input_file = os.path.join(dirname, INPUT_FILE_NAME)
output_file = os.path.join(dirname, OUTPUT_FILE_NAME)

# get links
terms = [line.rstrip('\n') for line in open(input_file) if not line.startswith('#') and line.strip()]

print("##########################################################")
print("#                  Tantum optimus testis                 #")
print("##########################################################\n")

f = open(output_file,"w+")

for term in terms:

    hops = 0
    url = PREFIX + term
    while True:

        if url == TARGET:
            vsklogger.debug("SIEG mit {} Hüpfern!".format(hops))
            break

        if hops > MAX_HOPS:
            vsklogger.warning("Ihr hop-Guthaben ist aufgebraucht!")
            hops = 'X'
            break
        try:
            url = get_first_article_link(url)
            #url = get_first_link(url)
        except Exception as ex:
            vsklogger.warning(ex)
            hops = 'E'
            break

        hops += 1
        vsklogger.info(">>> {}. hop ({})".format(hops, url))
    
    print("{} , {}".format(term , hops))
    f.write("{}, {}\n".format(PREFIX + term, hops))
    
print("\nAlea iacta est.")
f.close()