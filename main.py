import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urljoin
import logging


KEY_WORDS = ["America", "Europe", "Asia", "Africa", "Australia"]


def fetch_html(url, delay):
    # Supply the local path of web driver.
    # in this example we use chrome driver
    browser = webdriver.Chrome('/usr/local/bin/chromedriver')
    # Open the browser with the URL
    # a browser windows will appear for a little while
    browser.get(url)
    browser.implicitly_wait(delay)

    # Grab the rendered HTML
    html = browser.page_source

    # Close the browser
    browser.quit()

    return html


def crawl_text(url, delay):
    # wait for the page fully loaded and get the content
    raw_html = fetch_html(url, delay)
    soup = BeautifulSoup(raw_html, "html.parser")
    # remove HTML tags
    processed_text = soup.text
    return processed_text, soup


def remove_redundant(links):
    links = set(links)  # set removes duplicate
    redundants = ['#', '/']
    for redundant in redundants:
        try:
            links.remove(redundant)
        except Exception as e:
            logging.debug(e)

    return links


def remove_external_domain(homepage_url, subpage_urls):
    for subpage_url in subpage_urls:
        # Get absolute url
        subpage_url = urljoin(homepage_url, subpage_url)
        if not subpage_url.startswith(homepage_url):
            subpage_urls.remove(subpage_url)
    return subpage_urls


if __name__ == '__main__':
    df = pd.read_csv("./data/check_list.csv")
    # Add columns
    for kw in KEY_WORDS:
        df["'" + kw + "'" + " on homepage"] = False
        df[kw + " on subpage"] = False

    for index, row in df.iterrows():
        homepage_url = row['Website']
        # Crawl the HOMEPAGE
        homepage_text, soup = crawl_text(homepage_url, 1)

        # check in HOMEPAGE
        for kw in KEY_WORDS:
            if kw in homepage_text:
                df[kw + " on homepage"] = True

        subpage_urls = []
        for href in soup.findAll('a'):
            subpage_urls.append(href.get('href'))

        subpage_urls = remove_redundant(subpage_urls)
        subpage_urls = remove_external_domain(subpage_urls)

        for subpage_url in subpage_urls:
            # Crawl the SUBPAGE
            subpage_text, _ = crawl_text(subpage_url, 1)
            # check in SUBPAGE
            for kw in KEY_WORDS:
                if kw in subpage_text:
                    df["'" + kw + "'" + " on subpage"] = True

    # Output
    df.to_excel("output.xlsx")
