#!/usr/bin/env python
# coding: utf-8

# # 1. NASA Mars News


# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import os
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium import webdriver
import pandas as pd




def mars_news(browser):


    # URL of page to be scraped
    url = 'https://redplanetscience.com/'


    browser.visit(url)

    time.sleep(1)


    #HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')



    # Retrieve div with article title and paragraph text
    results = soup.find('div', class_="list_text")

    #Extract news title and paragraph text
    news_title = results.find("div", class_="content_title").text
    news_p = results.find("div", class_ ="article_teaser_body").text
    ## print(news_title)
    #  print (news_p)
    return news_title, news_p




# # 2. JPL Mars Space Images - Featured Image

def featured_image(browser):

   # Visit the url for the image
   image_url = "https://spaceimages-mars.com/"
   browser.visit(image_url)


   #HTML Object
   html_image = browser.html

   # Parse HTML with Beautiful Soup
   image_soup = bs(html_image, 'html.parser')


   # find the image url for the full size image
   results = image_soup.find("div", class_='header')
   full_image = results.find('div', class_='floating_text_area').a['href']


   # save a complete url string for this image
   featured_image_url = f'https://spaceimages-mars.com/{full_image}'
   return featured_image_url


   # # 3. Mars Facts



def mars_facts(browser):
   #mars facts url
   facts_url='https://galaxyfacts-mars.com/'
   browser.visit(facts_url)

   # Use Panda's `read_html` to parse the url
   tables = pd.read_html(facts_url)
   

   df = tables[0]
   df.columns = ['Description', 'Mars', 'Earth']
   
   # Convert dataframe into HTML format, add bootstrap
   return df.to_html(classes="table table-striped")


# # 4. Mars Hemispheres

def mars_hemisphere(browser):

    # Visit the url for the hemispheres
    hem_url = "https://marshemispheres.com/"
    browser.visit(hem_url)

    # create dictionary to store image url string and the hemisphere title
    hemisphere_image_urls = []

    #For loop to get titles and urls
    for i in range (1,5):
        results = {}
        xpath_link='//*[@id="product-section"]/div[2]/div[' + str(i) +']/a/img'
    
        #interact with browser
        browser.find_by_xpath(xpath_link).click()
        title = browser.find_by_xpath('//*[@id="results"]/div[1]/div/div[3]/h2').value
    
        img_url = browser.find_by_xpath('//*[@id="wide-image"]/div/ul/li[1]/a')['href']
    
        # Add extracts to the results dict
        results = {
            'title': title,
            'img_url': img_url
            }
    
        # Append results dict to hemisphere image urls list
        hemisphere_image_urls.append(results)
        browser.back()

   # Quit browser
    browser.quit()


    return hemisphere_image_urls



def scrape():
    executable_path =  {'executable_path': ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_p = mars_news(browser)
    featured_img_url = featured_image(browser)
    facts = mars_facts(browser)
    hemisphere_image_urls = mars_hemisphere(browser)
    

    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_img_url,
        "facts": facts,
        "hemispheres": hemisphere_image_urls}
       
    browser.quit()
    return mars_data 

if __name__ == "__main__":
    print(scrape())

