#!/usr/bin/env python3

from selenium import webdriver

starting_url = 'https://en.wikipedia.org/wiki/Special:Random'
article_selector = '#my-content-text'
exclude_link_parent_classes = ['hatnote', 'mw-collapsible']

driver = webdriver.Chrome()
driver.get(starting_url)

first_link = None
article_content = driver.find_element_by_css_selector(article_selector)
for link in article_content.find_elements_by_tag_name('a'):
    print(link.get_attribute('href'))
    link_parent = link.find_element_by_xpath('..')
    classes = link_parent.get_attribute('class')
    for exclude_class in exclude_link_parent_classes:
        print(exclude_class, classes)
        if exclude_class not in classes:
            first_link = link
            break
print(first_link.get_attribute('href'))
