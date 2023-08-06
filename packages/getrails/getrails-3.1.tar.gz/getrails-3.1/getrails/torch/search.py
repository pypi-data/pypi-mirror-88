#!/usr/bin/env python3
import mechanicalsoup

def go_onion(query):
    output = []
    # Connecting to torch
    browser = mechanicalsoup.StatefulBrowser()
    browser.set_user_agent('Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0')
    browser.open(f"https://torsearch.net/search?query={query}&page=1")

    # Crawler
    def change_page():
        for link in browser.get_current_page().select('ul.pagination li.page-item'):
            if link.get('active') == "": 
                position = int(link.text.replace('\n', ''))
                browser.open(f"https://torsearch.net/search?query={query}&page={position+1}")
                read_urls()

    def check():
        if browser.get_current_page().select('ul.pagination'):
            change_page()

    def read_urls():
        urls = browser.get_current_page().select('div.result a')
        if len(urls) > 0:
            for link in urls:
                output.append(link.get('href'))

            check()

    read_urls()
    return output


