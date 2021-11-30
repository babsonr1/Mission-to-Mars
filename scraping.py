import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
newsSoup = soup(html, 'html.parser')
slideElem = newsSoup.select_one('div.list_text')

slideElem.find('div', class_='content_title')

newsTitle = slideElem.find('div', class_='content_title').get_text()
newsTitle

newsp = slideElem.find('div', class_='article_teaser_body').get_text()
newsp

# ### Featured Images

url = 'https://spaceimages-mars.com'
browser.visit(url)

fullImageElem = browser.find_by_tag('button')[1]
fullImageElem.click()

html = browser.html
imgSoup = soup(html, 'html.parser')

imgUrlRel = imgSoup.find('img', class_='fancybox-image').get('src')
imgUrlRel

imgUrl = f'https://spaceimages-mars.com/{imgUrlRel}'
imgUrl

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

browser.quit()