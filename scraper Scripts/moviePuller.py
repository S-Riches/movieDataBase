# imports
from requests_html import HTMLSession, HTMLSession
import requests

# this function will get the 'free' to watch films from amazon prime, and then put them into a list to then filter through
def getPrimeFilms():
    primeMovies = []
    # create a HTML session object
    session = HTMLSession()
    # variable to contain the url
    url = 'https://www.amazon.co.uk/gp/video/search/ref=atv_sr_filter_p_n_entity_type?phrase=Included%20with%20Prime&ie=UTF8&pageId=default&queryToken=eyJ0eXBlIjoiZmlsdGVyIiwibmF2Ijp0cnVlLCJzZWMiOiJjZW50ZXIiLCJzdHlwZSI6InNlYXJjaCIsInFyeSI6InBfbl93YXlzX3RvX3dhdGNoPTc0NDg2NjIwMzEmbm9kZT0zMjgwNjI2MDMxJnNlYXJjaC1hbGlhcz1pbnN0YW50LXZpZGVvJnBfbl9lbnRpdHlfdHlwZT05NzM5OTUyMDMxIiwidHh0IjoiIiwiZmlsdGVyIjp7fSwib2Zmc2V0IjowLCJucHNpIjowLCJvcmVxIjoiZTJmZTQxMDUtNDBhYS00ZWUzLWFhMmMtZjg0NzU3NGE5NDJkOjE2NjE2MjU5ODQwMDAiLCJzdEtleSI6IntcInNic2luXCI6MCxcImN1cnNpemVcIjowLFwicHJlc2l6ZVwiOjB9Iiwib3JlcWsiOiJtanhETjhaSGRhVGVWWjVrTGVuSHJjWmF1cGpIV2JvZDRxV3BWcHphUWlBPSIsIm9yZXFrdiI6MX0%3D&queryPageType=browse'
    # create a request to pull the html for this page
    r = session.get(url)
    # note we also use these arguements for a few things - the sleep function gives the page some time to load, which stops the page returning nothing but js, along with keep page which allows interaction with browser pages through r.html.page, and scroll down that scrolls down the page
    r.html.render(sleep=5, script="window.scrollTo(0, document.body.scrollHeight);", reload=True, keep_page=True)
    # find this each of this class in a page and create a list
    mov = r.html.find('.tst-hover-title')
    # for each item in the list of the movies
    for item in mov:
        #append the list
        primeMovies.append(item.text)
    # use this or else headless chromium pages wont close which drains memory
    r.close()
    print("Prime Video Scrape /")
    return primeMovies
    
def getNowTVFilms():
    nowMovies = []
    # create a HTML session object
    session = HTMLSession()
    # variable to contain the url
    url = 'https://www.nowtv.com/stream/all-movies'
    # create a request to pull the html for this page
    r = session.get(url)
    # now the r object is (due to prime video being a javascript focused page) a lot of code and not a lot of information, so we have to use the render function
    # TODO tried to get the data from now TV AJAX but keep getting error code 400, bit stumped at the moment but i can still get the data via scraping the page - however at a slower speed.
    r.html.render()
    # find this each of this class in a page and create a list
    mov = r.html.find('.ib-card-title')
    # for each item in the list of the movies
    for item in mov:
        # add to list
        nowMovies.append(item.text)
    for i in range(1, 21):
        # dirty fix atm to get all of the films needed for this website
        url = 'https://www.nowtv.com/stream/all-movies/page/'+str(i)
        r = session.get(url)
        mov = r.html.find('.ib-card-title')
        for item in mov:
            nowMovies.append(item.text)
    r.close()
    print("NowTV Scrape /")
    return nowMovies

def makeJsonRequest(url):
    # due to channel 4 having a show more button, to get all content i am going to pull the JSON for each page and filter through it this way
    # create a request to the url
    response = requests.get(url)
    # prints incase of an error
    response.raise_for_status()
    # formats the response as a JSON
    jsonResponse = response.json()
    # allows me to key to only the important information
    return jsonResponse


def getAll4Films():
    all4Movies = []
    session = HTMLSession()
    url = 'https://www.channel4.com/categories/film'
    r = session.get(url)
    r.html.render()
    titles = r.html.find('.all4-slice-item__title')
    for i in titles:
        all4Movies.append(i.text)
        
    # scrape the other pages - note if they offset more this will only do these pages, so there is probably a better way to do this
    for i in range(20, 100, 20):
        json = makeJsonRequest('https://www.channel4.com/categories/film?json=true&offset='+str(i)) 
        # go through the dictioary keys
        for x in json["brands"]["items"]:
            # append list with titles
            all4Movies.append(x['labelText'])
    r.close()
    print("All4 Scrape /")
    return all4Movies

