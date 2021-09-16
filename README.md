> # Mars Data Flask App

![hero_image.jpg](images/hero_image.jpg)

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

### Scraping  images for mars hemispheres

* Load the base url for the image

```sh
    image_base_path = 'https://spaceimages-mars.com/'
```

* Load the URL to the splinter browser and then parse the html page.

```sh
    # base hemisphere URL
    hemisphere_url = 'https://marshemispheres.com/'
    # check the html
    browser.visit(hemisphere_url)
    # load the html into the parser
    html_hemis = browser.html
    hem_soup = BeautifulSoup(html_hemis, 'html.parser')
```
* Scrape the hemisphere descriptions and create a list of hemisphere image links

```sh
    # scrape html for list of hemisphere
    hem_title = [title.find('h3').text for title in hem_soup.find_all('div', class_ = 'description')]
    # scrap html for list of separate hemisphere url
    hem_ref = [img_url.find('a')['href'] for img_url in hem_soup.find_all('div', class_ = 'description')]
```
* Create a function that iterates through each hemisphere image links and scrape the link for the images. 

```sh
     def img_url_parser(hem_url):
        hem_url = hemisphere_url +hem_url
        browser.visit(hem_url)
        hem_img_soup = BeautifulSoup(browser.html,'html.parser')
        img_url = hemisphere_url + hem_img_soup.find_all('li')[1].find('a')['href']
        return img_url
```

* Use the function to scrape the links

```sh
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
```
### Load all the scraped information into a dictionary for MongoDB

* Now we load the information into MongoDB

```sh
    mars_dict = {
        "news_title": news_title,
        "news_body": news_body,
        "featured_image": featured_image_url,
        "mars_fact_table": mars_table_html,
        "mars_hemisphere_images":hemisphere_image_urls
    }
    print("mars_dict populated")
    return mars_dict
```

### Setup the config file for MongoDB credentials

* Create the config.py
1. Import the ChromeDriver Manager
2. Create the chrome_driver_path
3. Create the mongo_url

* add the config file to gitignore. 

### Create a flask server to load, display, and update scraped information to MongoDB

1. Load the dependencies.

```sh
    from flask import Flask, render_tmeplate, redirect
    from flask_pymongo import PyMongo
    from scrape_mars import scrape
    from config import mongo_uri
```

2. Initialize the flask application

```sh
    app = Flask(__name__)
    app.config['MONGO_URI'] = mongo_uri
    mongo = PyMongo(app)
```

3. Create the index.html and load it into the templates folder for render_template to pull from.

* slot in the various dictionary objects as appropriate for display:

```sh
    <body>
  <div class="container">

    <div class="jumbotron text-center border-bottom">
      <h1 class="font-weight-bold">Mission to Mars</h1>
      <p><a class="btn btn-primary btn-lg" href="../scrape" role="button">Scrape New Data</a></p>
    </div>
    <div class="row">
      <div class="col-md-12">
        <h2><u>Latest Mars News</u></h2>
      </div>
    </div>
  </br>
    <div class="row">
      <div class="col-md-12">
        <h4>{{mars_infoHTML.news_title}}</h4>
        <p>{{mars_infoHTML.news_body}}</p>
      </div>
    </div>
  <hr>
    <div class="row">
      <div class="col-md-8 border">
        <h2 class=""><u>Featured Mars Image</u></h2> 
        </br>
        <img src={{mars_infoHTML.featured_image}} alt="Features Mars Image">
      </div>
        <div class="col-md-4 border">
          <h5>Mars Facts</h5>
            {{ mars_infoHTML.mars_fact_table | safe }}
        </div>
      </div>
    </div>
  <hr>
    <div class="row">
      <div class="col-md-8 offset-4">
        <h2 class="align-items-center"><u>Mars hemispheres</u></h2>  
      </div>
    </div>
    </br>
    <div class="row">       
            {% for hemisphere in mars_infoHTML.mars_hemisphere_images %} 
              <div class="col-3 border">
              </br>
                    <div>
                      <img src="{{ hemisphere.img_url | safe }}" class = "img-fluid">
                    </div>

                    <div>
                      <h4> {{ hemisphere.title | safe }} </h4>  
                    </div>
            
              </div>
            {% endfor %}
    </div> 
  <hr>
</body>

```

4. Build the flask routes

* We need two routes:
* Homepage

```sh
    @app.route("/")
    def index():
        mars_information = mongo.db.mars_information.find_one()
        return render_template("index.html", mars_infoHTML = mars_information)
```

* Scraping route

```sh   
    @app.route("/scrape")
    def mars_scrape():
        mars_information = mongo.db.mars_information
        mars_data_new = scrape()
        mars_information.update({}, mars_data_new, upsert = True)
        print("db information updated")
        return redirect("/", code = 302)
```

5. Lastly, we will initialize the app and configure its debug behavior.

```sh
    if __name__ == "__main__":
        app.run(debug =)
```
