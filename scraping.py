from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrapeAll():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    newsTitle, newsParagraph = marsNews(browser)

    data = {
        "news_title": newsTitle,
        "news_paragraph": newsParagraph,
        "featured_image": featuredImage(browser),
        "facts": marsFacts(),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data


def marsNews(browser):
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    newsSoup = soup(html, 'html.parser')

    try:
        slideElem = newsSoup.select_one('div.list_text')
        newsTitle = slideElem.find('div', class_='content_title').get_text()
        newsp = slideElem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return newsTitle, newsp


def featuredImage(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    fullImageElem = browser.find_by_tag('button')[1]
    fullImageElem.click()

    # Parse the resulting html with soup
    html = browser.html
    imgSoup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        imgUrlRel = imgSoup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    imgUrl = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{imgUrlRel}'

    return imgUrl

def marsFacts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrapeAll())