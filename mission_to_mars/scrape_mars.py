# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from selenium import webdriver
import pandas as pd
import time





def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Create a dictionary to store the datas
    mars_dict = {}


    #### NASA MARS NEWS ####
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    news_html = browser.html
    news_soup = BeautifulSoup(news_html, 'lxml')
    news_title = news_soup.find("div", class_= "content_title").text
    news_paragraph = news_soup.find("div", class_ = "article_teaser_body").text
    mars_dict['news_title'] = news_title
    mars_dict['news_paragraph'] = news_paragraph


    #### JPL MARS SPACE IMAGES ####
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    image_html = browser.html
    image_soup = BeautifulSoup(image_html,'lxml')
    jpl_image = image_soup.find('figure', class_='lede').a['href']
    featured_image_url = (f'https://www.jpl.nasa.gov{jpl_image}')
    mars_dict['featured_image_url'] = featured_image_url


    #### MARS WEATHER ####
    tweet_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_weather_url)
    tweet_html = browser.html
    weather_soup = BeautifulSoup(tweet_html, 'lxml')
    latest_weather = weather_soup.find('div', class_= 'js-tweet-text-container')
    mars_weather = latest_weather.find('p', class_= 'TweetTextSize').text
    mars_dict['mars_weather'] = mars_weather


    #### MARS FACTS ####
    mars_fact_url = 'https://space-facts.com/mars'
    browser.visit(mars_fact_url)
    mars_fact_html = browser.html
    mars_soup = BeautifulSoup(mars_fact_html, 'lxml')
    tables = pd.read_html(mars_fact_url)
    mars_fact_df = tables[1]
    mars_final_df = mars_fact_df.rename(columns={0:"Parameters",1:"Values"})
    mars_final_df = mars_fact_df.to_html(header = False, index = False)
    mars_final_df.replace('\n', '')
    mars_dict['mars_final_df'] = mars_final_df


    #### MARS HEMISHPERES ####
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    

    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'lxml')
    base_url ="https://astrogeology.usgs.gov"

    image_list = hemisphere_soup.find_all('div', class_='item')

    # Create list to store dictionaries of data
    hemisphere_image_urls = []

    # Loop through each hemisphere and click on link to find large resolution image url
    for image in image_list:
        hemisphere_dict = {}
        
        href = image.find('a', class_='itemLink product-item')
        link = base_url + href['href']
        browser.visit(link)
        
        time.sleep(2)
        
        hemisphere_html2 = browser.html
        hemisphere_soup2 = BeautifulSoup(hemisphere_html2, 'lxml')
        
        img_title = hemisphere_soup2.find('div', class_='content').find('h2', class_='title').text
        hemisphere_dict['title'] = img_title
        
        img_url = hemisphere_soup2.find('div', class_='downloads').find('a')['href']
        hemisphere_dict['url_img'] = img_url
        
        # Append dictionary to list
        hemisphere_image_urls.append(hemisphere_dict)
        
    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_dict

