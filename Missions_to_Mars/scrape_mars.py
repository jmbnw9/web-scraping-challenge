from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import os
import requests


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/Users/Janelle Goddard/Downloads/chromedriver_win32/chromedriver"}
    return Browser("chrome", **executable_path)

mars_data={}

def scrape_info():
    browser = init_browser()

    # Visit mars websites

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Scrape the News title & paragraph
    stepone = soup.find('ul', class_='item_list')

    steptwo = stepone.find('li', class_='slide')
    news_title = steptwo.find('div', class_='content_title').text
    news_p = steptwo.find('div', class_='article_teaser_body').text

    # Scrape the featured image
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    feature_image = soup.find('div', class_='floating_text_area').a['href']
    featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + feature_image

    # Scrape the mars table
    url = 'https://space-facts.com/mars/'

    mars_table = pd.read_html(url)
    mars_table[0]
    mars_html_table = mars_table[0].to_html()

    # Scrape the mars hempispheres
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    html_hemisphere = browser.html
    soup = BeautifulSoup(html_hemisphere, 'html.parser')
    hemispheres = soup.find_all('div', class_='item')
    # Create an empty list to hold all the hempisphere urls
    hemisphere_images = []
    # store the main url
    hemisphere_url_main = 'https://astrogeology.usgs.gov'
    # Loop through the items
    for i in hemispheres:
        title = i.find("h3").text
    # Save the link that goes to the full image website
        hemisphere_image_url = i.find("a", class_="itemLink product-item")["href"]
        browser.visit(hemisphere_url_main + hemisphere_image_url)
        hemisphere_image_html = browser.html
        soup = BeautifulSoup(hemisphere_image_html, 'html.parser')
        img_url = hemisphere_url_main + \
            soup.find("img", class_="wide-image")["src"]
    # #Append the dictionary with the image url string and the hemisphere title to a list
        hemisphere_images.append({"title": title, "img_url": img_url})
   
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "feature_image": feature_image,
        "mars_html_table": mars_html_table,
        "hemisphere_images": hemisphere_images
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
