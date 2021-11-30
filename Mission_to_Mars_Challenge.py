#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


html = browser.html
newsSoup = soup(html, 'html.parser')
slideElem = newsSoup.select_one('div.list_text')


# In[5]:


slideElem.find('div', class_='content_title')


# In[6]:


newsTitle = slideElem.find('div', class_='content_title').get_text()
newsTitle


# In[7]:


newsp = slideElem.find('div', class_='article_teaser_body').get_text()
newsp


# ### Featured Images

# In[8]:


url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


fullImageElem = browser.find_by_tag('button')[1]
fullImageElem.click()


# In[10]:


html = browser.html
imgSoup = soup(html, 'html.parser')


# In[11]:


imgUrlRel = imgSoup.find('img', class_='fancybox-image').get('src')
imgUrlRel


# In[12]:


imgUrl = f'https://spaceimages-mars.com/{imgUrlRel}'
imgUrl


# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


# ### Deliverable One

# In[15]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[34]:


# 2. Create a list to hold the images and titles.
hemisphereImageUrls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
imgSoup = soup(html, 'html.parser')
imageUrlTable = imgSoup.find_all('img', class_='thumb')
for tag in imageUrlTable:
    hemisphereImageUrls.append(tag.get('src'))


# In[35]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphereImageUrls


# In[36]:


# 5. Quit the browser
browser.quit()


# In[ ]:




