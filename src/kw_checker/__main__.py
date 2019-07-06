import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urljoin
from datetime import datetime
from kw_checker.cfg import logger, \
    WEBSITES_DATA_FILEPATH, KEY_WORDS, CHROMEDRIVER_PATH

# Supply the local path of web driver.
# in this example we use chrome driver
chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chromeOptions.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(CHROMEDRIVER_PATH, options=chromeOptions)
# NOTE: remember to quit the browser with `browser.quit()`


def fetch_html(url, delay):
    # Open the browser with the URL
    # a browser windows will appear for a little while
    browser.get(url)
    browser.implicitly_wait(delay)

    # Grab the rendered HTML
    html = browser.page_source

    return html


def crawl_text(url, delay):
    logger.info("Processing %s" % url)
    # Wait for the page fully loaded and get the content
    raw_html = fetch_html(url, delay)
    soup = BeautifulSoup(raw_html, "html.parser")
    # Remove HTML tags
    processed_text = soup.text
    return processed_text, soup


def ignore_redundant_urls(urls):
    urls = set(urls)  # set removes duplicate
    redundants = ['#', '/']
    for redundant in redundants:
        try:
            urls.remove(redundant)
        except Exception as e:
            logger.warnning(e)

    return urls


def remove_external_domains(homepage_url, subpage_urls):
    valid_subpage_urls = []
    for subpage_url in subpage_urls:
        # Get absolute url
        subpage_url = urljoin(homepage_url, subpage_url)
        if subpage_url.startswith(homepage_url):
            valid_subpage_urls.append(subpage_url)
    return valid_subpage_urls


def check(datapath, keywords):
    df = pd.read_csv(datapath)
    # Add columns
    for kw in keywords:
        df["'" + kw + "'" + " on homepage"] = False
        df[kw + " on subpage"] = False

    for index, row in df.iterrows():
        try:
            homepage_url = row['Website']
            # Crawl the HOMEPAGE
            homepage_text, soup = crawl_text(homepage_url, 1)

            # Check in HOMEPAGE
            for kw in keywords:
                if kw in homepage_text:
                    df[kw + " on homepage"] = True

            subpage_urls = []
            for href in soup.findAll('a'):
                subpage_urls.append(href.get('href'))

            subpage_urls = ignore_redundant_urls(subpage_urls)
            subpage_urls = remove_external_domains(homepage_url, subpage_urls)

            for subpage_url in subpage_urls:
                # Crawl the SUBPAGE
                subpage_text, _ = crawl_text(subpage_url, 1)
                # Check in SUBPAGE
                for kw in keywords:
                    if kw in subpage_text:
                        df["'" + kw + "'" + " on subpage"] = True
        except Exception as e:
            logger.warnning(e)

    return df


def main():
    now = datetime.now()
    df = check(WEBSITES_DATA_FILEPATH, KEY_WORDS)
    # Output
    df.to_excel("./output_%s.xlsx" % str(now))
    browser.quit()


if __name__ == '__main__':
    main()
