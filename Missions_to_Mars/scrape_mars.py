import pandas as pd
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def scrape():
    dict_scrape = {}

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    dict_scrape['news_title'] = news_title
    dict_scrape['news_p'] = news_p
    browser.quit()


    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    image_path = soup.find('img', class_='headerimage fade-in')
    featured_image_url = url + image_path['src']
    dict_scrape['featured_mars_image'] = featured_image_url
    browser.quit()

    url = 'https://galaxyfacts-mars.com/'
    table = pd.read_html(url)
    mars_facts_df = table[0]
    mars_facts_df.columns = mars_facts_df.iloc[0]
    mars_facts_df = mars_facts_df.reset_index(drop=True)
    mars_html = mars_facts_df.to_html('mars_facts.html')
    dict_scrape['mars_facts'] = mars_html
    browser.quit()

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    hemisphere_images = []
    results = soup.find_all('div', class_='description')
    for result in results:
        hemisphere_dict = {}
        
        title = result.find('h3').text
        item_link = result.find('a', class_='itemLink product-item')['href']
        browser.links.find_by_partial_text(title).click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        rel_path = soup.find('img', class_= 'wide-image')['src']
        abs_path = f'{url}/{rel_path}'
        browser.visit(url)
        hemisphere_dict['title'] = title
        hemisphere_dict['img_url'] = abs_path
        hemisphere_images.append(hemisphere_dict)
        browser.back()
        dict_scrape['hemisphere_images'] =  hemisphere_images
    browser.quit() 