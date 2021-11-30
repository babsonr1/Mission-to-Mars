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
        "last_modified": dt.datetime.now(),
        "image_url": hemisphereData()
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
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    fullImageElem = browser.find_by_tag('button')[1]
    fullImageElem.click()

    html = browser.html
    imgSoup = soup(html, 'html.parser')

    try:
        imgUrlRel = imgSoup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    imgUrl = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{imgUrlRel}'

    return imgUrl

def marsFacts():
    try:
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html(classes="table table-striped")

def hemisphereData(browser):
    try:
        hemisphereImageUrls = []
        html = browser.html
        imgSoup = soup(html, 'html.parser')
        imageUrlTable = imgSoup.find_all('img', class_='thumb')
        for tag in imageUrlTable:
            hemisphereImageUrls.append(tag.get('src'))
        return hemisphereImageUrls
    except AttributeError:
        return None


if __name__ == "__main__":
    print(scrapeAll())