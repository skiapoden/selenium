#!/usr/bin/env python3

from selenium import webdriver

starting_url = 'https://en.wikipedia.org/wiki/Special:Random'
article_selector = 'div.mw-parser-output'
exclude_link_classes = ['image']
exclude_link_parent_classes = ['hatnote', 'mw-collapsible']

driver = webdriver.Chrome()

def get_first_article_link(article_url):
    return get_first_link_url(article_url, exclude_link_classes, exclude_link_parent_classes)

def get_first_link_url(url, class_exclude_list, parent_class_exclude_list):
    driver.get(url)
    article_content = driver.find_element_by_css_selector(article_selector)
    first_link = None
    for link in article_content.find_elements_by_tag_name('a'):
        link_parent = link.find_element_by_xpath('..')

        # exclude classes of the link itself
        classes = link.get_attribute('class')
        if classes != '':
            for exclude_class in class_exclude_list:
                if exclude_class in classes:
                    continue

        # exclude classes of the parent object
        # TODO: implement recursively
        parent_classes = link_parent.get_attribute('class')
        if parent_classes == '':
            first_link = link
            break
        for exclude_class in parent_class_exclude_list:
            if exclude_class not in parent_classes:
                first_link = link
                break

    if first_link == None:
        return ''
    return first_link.get_attribute('href')
