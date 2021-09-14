from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from config import chrome_driver_path

def browser_initiation():
    return Browser("chrome", **chrome_driver_path, headless = False)

def scrape():
    #initiate the browser to load URL data
    browser_initiation()

    # retrieving latest mars news
    # mars news url
    mars_news_url = 'https://mars.nasa.gov/news/'
    # load news URL into the browser
    browser.visit(mars_news_url)

    # load the html into the parser
    news_html = browser.html
    soup_news = BeautifulSoup(news_html, 'html.parser')

    # retrieving latest news page title and body
    news_title = soup_news.find('div', class_='list_text').find('a').text
    print("news_title retrival complete")
    news_body = soup_news.find('div', class_= 'article_teaser_body').text
    print("news_body retrieval complete")


    # retrieving mars images
    # base image url
    image_base_path = 'https://spaceimages-mars.com/'

    # check the html
    browser.visit(image_base_path)
    # load the html into the parser
    html_img = browser.html
    images_soup = BeautifulSoup(html_img, 'html.parser')# retrieve featured image link
    img_path = images_soup.find('img', class_ = 'headerimage fade-in')['src']
    featured_image_url = image_base_path + img_path
    print("featured_image_url retrieval complete")

    # retrieving mars facts
    # base mars fact URL
    mar_fact_url = 'https://galaxyfacts-mars.com'
    html_table_string = pd.read_html(mar_fact_url)
    print("html_table_string retrieval complete")

    # retreive mars hemisphere information
    # base hemisphere URL
    hemisphere_url = 'https://marshemispheres.com/'
    # check the html
    browser.visit(hemisphere_url)
    # load the html into the parser
    html_hemis = browser.html
    hem_soup = BeautifulSoup(html_hemis, 'html.parser')
    # scrape html for list of hemisphere
    hem_title = [title.find('h3').text for title in hem_soup.find_all('div', class_ = 'description')]
    # scrap html for list of separate hemisphere url
    hem_ref = [img_url.find('a')['href'] for img_url in hem_soup.find_all('div', class_ = 'description')]

    # create a function to extract the indivisual url based on each hemisphere url
    def img_url_parser(hem_url):
        hem_url = hemisphere_url +hem_url
        browser.visit(hem_url)
        hem_img_soup = BeautifulSoup(browser.html,'html.parser')
        img_url = hemisphere_url + hem_img_soup.find_all('li')[1].find('a')['href']
        return img_url

    # apply the function to each itmes in the hemisphere url list
    img_url = list(map(img_url_parser, hem_ref))
    # create the list of hemisphere dictionaries
    hemisphere_image_urls = []
    if len(hem_title) == len(img_url):
        for index in range(len(hem_title)):
            hemisphere_image_urls.append(
            { 'title' : hem_title[index],
                'img_url': img_url[index]}
            )
    print("hemisphere_image_urls retrieval complete")
        
    mars_dict = {
        "news_title": news_title,
        "news_body": news_body,
        "featured_image": featured_image_url,
        "mars_fact_table": html_table_string,
        "mars_hemisphere_images":hemisphere_image_urls
    }
    print("mars_dict populated")
    return mars_dict