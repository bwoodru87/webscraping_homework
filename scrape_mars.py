from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape():
    mars_data = {}

    url = 'https://mars.nasa.gov/news/'
    response_news = requests.get(url)
    soup_news = BeautifulSoup(response_news.text, 'html.parser')

    titles = []
    for text in soup_news.findAll('div',attrs={"class":"content_title"}):
        a = text.get_text()
        titles.append(a)
    
    content = []
    for text in soup_news.findAll('div',attrs={"class":"rollover_description_inner"}):
        a = text.get_text()
        content.append(a)

    recent_title = titles[0]
    recent_content = content[0]

    mars_data["latest_title"] = recent_title
    mars_data["latest_content"] = recent_content


    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response_image= requests.get(url_image)
    soup_image = BeautifulSoup(response_image.text, "html.parser")
    image = soup_image.find_all('a',class_='fancybox')
    image[0]
    link = image[0]["data-fancybox-href"]
    full_link = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars" + link
    mars_data["full_image"] = full_link



    url_weather = 'https://twitter.com/marswxreport?lang=en'
    response_weather = requests.get(url_weather)
    soup_weather = BeautifulSoup(response_weather.text, 'html.parser')
    
    tweets = []
    for text in soup_weather.findAll('p',attrs={"class":"TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}):
        a = text.get_text()
        tweets.append(a)

    first_tweet = tweets[0]
    mars_data["mars_weather"] = first_tweet



    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url_hemi)
    soup_hemi = BeautifulSoup(response.text, 'html.parser')
    images = soup_hemi.find_all('div',class_="item")

    hemi_title = []
    hemi_url = [] 
    for i in images:
        title=i.find('h3').text.replace('Enhanced',"")
        link=i.find('a',class_='itemLink product-item')
        new_link = link['href'].replace('/search/map/','https://astropedia.astrogeology.usgs.gov/download/')
        final_link = new_link + ".tif/full.jpg"
        hemi_title.append(title)
        hemi_url.append(final_link)

    hemisphere_image_urls = [
    {"title": hemi_title[0], "img_url": hemi_url[0]},
    {"title": hemi_title[1], "img_url": hemi_url[1]},
    {"title": hemi_title[2], "img_url": hemi_url[2]},
    {"title": hemi_title[3], "img_url": hemi_url[3]},
    ]
    mars_data["hemi_urls"] = hemisphere_image_urls


    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_df = tables[0]
    mars_df.rename(columns={0:"Category",1:"Mars Info"})
    html_table = mars_df.to_html()
    new_html = html_table.replace('\n', '')
    
    mars_data["mars_data_table"] = new_html

    return mars_data
