> # Mars Data Flask App

![hero_image.jpg](Images/hero_image.jpg)

### Backgroud

Flask is a powerful tool to scrape and render data on the web to be shared. We will practice Flask using data from mars to render otno the web while storing the data inside a local server through MongoDb.

### Scraping Mars Data

The Mars Dataset will be coming from various locations on the web. We will be scraping from the following URL:

1. Lates News From Mars:<a href = 'https://mars.nasa.gov/news/'>`Link`</a> 
<br>
We will be retrieving the title and text from the latest mars news on the webpage. 

2. Featured Image of Mars<a href = 'https://spaceimages-mars.com/'>`Link`</a> 
<br>
We will be retrieving the Featured Image of Mars on this website.

3. Facts about Mars<a href = 'https://galaxyfacts-mars.com'>`Link`</a> 
<br>
We will be retrieving general information of Mars from this website.

4. Facts about Mars<a href = 'https://marshemispheres.com/'>`Link`</a> 
<br>
We will be retrieving pictures from each hemisphere of Mars


## Technology

1. splinter
2. BeautifulSoup
3. Pandas
4. Pymonogo
5. flask_pymongo
6. Flask
7. webdriver_manager.chrome

* Importing the dependencies
```sh
    from splinter import Browser
    from bs4 import BeautifulSoup
    import pandas as pd
    import pymongo
    from flask import Flask, rendter_template, redirect
    from flask_pymongo import PyMongo
    from webdriver_manager.chrome import ChromeDriver
```
We will first need to initiate the browser

### Scraping Mars News

* Load the base url for news

```sh
    mars_news_url = 'https://mars.nasa.gov/news/'
```

* Load the URL to the splinter browser and then parse the html page.

```sh
    browser.visit(mars_news_url)
    news_html = browser.html
    soup_news = BeautifulSoup (news_html, "html.parser")
```
* Isolate the title and text for the latest news from mars

```sh
    news_title = soup_news.find('div', class_='list_text').find('a').text
    print("news_title retrival complete")
    news_body = soup_news.find('div', class_= 'article_teaser_body').text
```

### Scraping Feature Image from Mars

* Load the base url for the image

```sh
    image_base_path = 'https://spaceimages-mars.com/'
```

* Load the URL to the splinter browser and then parse the html page.

```sh
    browser.visit(image_base_path)
    news_html = browser.html
    soup_news = BeautifulSoup (news_html, "html.parser")
```
* Isolate the directory of the image and compile the full url for the image.

```sh
    img_path = images_soup.find('img', class_ = 'headerimage fade-in')['src']
    featured_image_url = image_base_path + img_path
```
### Scraping Feature Image from Mars

* Load the base url for the image

```sh
    image_base_path = 'https://spaceimages-mars.com/'
```

* Load the URL to the splinter browser and then parse the html page.

```sh
    browser.visit(image_base_path)
    news_html = browser.html
    soup_news = BeautifulSoup (news_html, "html.parser")
```
* Isolate the directory of the image and compile the full url for the image.

```sh
    img_path = images_soup.find('img', class_ = 'headerimage fade-in')['src']
    featured_image_url = image_base_path + img_path
```
