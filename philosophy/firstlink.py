#!/usr/bin/env python3

from selenium import webdriver
import re

driver = webdriver.Chrome()

"""
The first link of an article can be found through this path:

div#content
    div#bodyContent
        div#mw-content-text
            div.mw-parser-output
                p:first-of-type
"""
def get_first_article_link(url):
    driver.get(url)

    first_link = None
    div_content = driver.find_element_by_css_selector('div#mw-content-text')
    div_output = div_content.find_element_by_css_selector('div.mw-parser-output')
    paragraphs = div_output.find_elements_by_tag_name('p')
    paragraphs = [p for p in paragraphs if not contained(['mw-empty-elt'], p.get_attribute('class'))]
    links = paragraphs[0].find_elements_by_tag_name('a')
    links = [l for l in links if len(l.get_attribute('class')) == 0]

    exclude_classes = ['internal', 'mw-redirect']
    exclude_href_patterns = ['.*upload.wikimedia.org.*', '.*/wiki/File:.*', '^#.*', '.*#cite.*',
            '.*Help:IPA/.*']
    links = [l for l in links if not contained(exclude_classes, l.get_attribute('class'))]
    links = [l for l in links if not matches(exclude_href_patterns, l.get_attribute('href'))]

    if len(links) > 0:
        return links[0].get_attribute('href')
    raise Exception('unable to find first article link')

def contained(exclude_items, items):
    for exclude in exclude_items:
        if exclude in items:
            return True
    return False

def matches(patterns, string):
    for pattern in patterns:
        p = re.compile(pattern)
        if p.match(string):
            return True
    return False
