# imports
from requests_html import HTMLSession

# work out how to make this async because atm it takes years to get movie info back for one site, let alone multiple

# this function will get the free to watch films from amazon prime, and then put them into a list to then filter through
def getPrimeFilms():
    # create a HTML session object
    session = HTMLSession()
    # variable to contain the url
    url = 'https://www.amazon.co.uk/gp/video/search/ref=atv_sr_filter_p_n_entity_type?phrase=Included%20with%20Prime&ie=UTF8&pageId=default&queryToken=eyJ0eXBlIjoiZmlsdGVyIiwibmF2Ijp0cnVlLCJzZWMiOiJjZW50ZXIiLCJzdHlwZSI6InNlYXJjaCIsInFyeSI6InBfbl93YXlzX3RvX3dhdGNoPTc0NDg2NjIwMzEmbm9kZT0zMjgwNjI2MDMxJnNlYXJjaC1hbGlhcz1pbnN0YW50LXZpZGVvJnBfbl9lbnRpdHlfdHlwZT05NzM5OTUyMDMxIiwidHh0IjoiIiwiZmlsdGVyIjp7fSwib2Zmc2V0IjowLCJucHNpIjowLCJvcmVxIjoiZTJmZTQxMDUtNDBhYS00ZWUzLWFhMmMtZjg0NzU3NGE5NDJkOjE2NjE2MjU5ODQwMDAiLCJzdEtleSI6IntcInNic2luXCI6MCxcImN1cnNpemVcIjowLFwicHJlc2l6ZVwiOjB9Iiwib3JlcWsiOiJtanhETjhaSGRhVGVWWjVrTGVuSHJjWmF1cGpIV2JvZDRxV3BWcHphUWlBPSIsIm9yZXFrdiI6MX0%3D&queryPageType=browse'
    # create a request to pull the html for this page
    r = session.get(url)
    # now the r object is (due to prime video being a javascript focused page) a lot of code and not a lot of information, so we have to use the render function
    # note we also use these arguements for a few things - the sleep function gives the page some time to load, which stops the page returning nothing but js, along with keep page which allows interaction with browser pages through r.html.page, and scroll down that scrolls down the page
    # note #2 i realise now it would be much more efficient to just get the content from AJAX instead of scrolling to the bottom but IIABDFI
    r.html.render(sleep=1, scrolldown=50)
    # find this each of this class in a page and create a list
    movies = r.html.find('.av-beard-title-link')
    #TODO perhaps get the year from the scrape and assign it in the dictionary
    # for each item in the list of the movies
    for item in movies:
        #create a dictionary called movie
        movie = {
            # set the movie title as the text
            'Prime Movie Title' : item.text
        }
        # print it
        print(movie)
    
def getNowTVFilms():
    # create a HTML session object
    session = HTMLSession()
    # variable to contain the url
    url = 'https://www.nowtv.com/stream/all-movies'
    # create a request to pull the html for this page
    r = session.get(url)
    # now the r object is (due to prime video being a javascript focused page) a lot of code and not a lot of information, so we have to use the render function
    # TODO this website uses pages that load on scroll to display different films - therefore i need to write code to work out how many films are on one page - then to change page after that many films are scraped
    r.html.render(sleep=1)
    # find this each of this class in a page and create a list
    movies = r.html.find('.ib-card-title')
    # for each item in the list of the movies
    for item in movies:
        #create a dictionary called movie
        movie = {
            # set the movie title as the text
            'NowTV Movie Title' : item.text
        }
        # print it
        print(movie)
        
#getPrimeFilms()
getNowTVFilms()