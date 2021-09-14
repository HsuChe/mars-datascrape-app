from webdriver_manager.chrome import ChromeDriverManager

chrome_driver_path = {'executable_path': ChromeDriverManager().install()}
mongo_uri = "mongodb://localhost:27017/mars_app"