from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

data_mars = {}
def init_browser():
   
    executable_path = {"executable_path": 'C:/chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

 
def latest_new():
    browser = init_browser()

         
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Get the latest news
    news = soup.find("div", class_='list_text')
    news_title = news.find("div", class_="content_title").text
    news_p = news.find("div", class_="article_teaser_body").text

    data_mars['news_title'] = news_title
    data_mars['news_p'] = news_p
            
    browser.quit()
    return (data_mars)


def featured_img():
    browser = init_browser()
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')
    
    featured_image= soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image
        
    data_mars['featured_img'] = featured_image_url

    # Close the browser after scraping
    browser.quit()
    return (data_mars)

def mars_facts():
    import pandas as pd
    browser = init_browser()
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    
    tables = pd.read_html(url)
    df_mars_profile = pd.DataFrame(tables[0])
    df_mars_profile.columns = ['Profile', 'Mars']
    df_mars_profile=df_mars_profile.set_index('Profile')
    html_mars_table = df_mars_profile.to_html(index_names= False, header =True, sparsify=True, table_id = "table", classes= "table table-striped"  ).replace('\n', '')
    data_mars['mars_facts'] = html_mars_table

    # Close the browser after scraping
    browser.quit()

    return (data_mars)

def mars_hemispheres_img():
    usgs_url = {"marineris_img":'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced',
                "cerberus_img":'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
                "schiaparelli_img":'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
                "syrtis_img":'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'}

    for hem_name,url in usgs_url.items():
            browser = init_browser()
            browser.visit(url)

            # Scrape page into Soup
            html = browser.html
            soup = bs(html, 'html.parser')
            img_url = (soup.find_all('div', class_='downloads'))[0].ul.li.a.get('href')
            print(img_url)

            if hem_name == "marineris_img":
                data_mars["marineris_img"] = img_url
            elif hem_name == "cerberus_img":
                data_mars["cerberus_img"] = img_url
            elif hem_name == "schiaparelli_img":
                data_mars["schiaparelli_img"] = img_url
            else:
                data_mars["syrtis_img"] = img_url
     
            browser.quit()
    
    return (data_mars)

