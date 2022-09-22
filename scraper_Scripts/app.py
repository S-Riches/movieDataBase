#imports
import signal
import json
import time
import moviePuller
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import os
import mysql.connector
from os.path import join, dirname
from apscheduler.schedulers.background import BackgroundScheduler # adds support for scheduling functions to be run - in this use case i need to prune and rescrape everyday

# this is for the environment variables - meaning i dont have to share the passwords and hostnames for my servers - v good
dotEnvPath = join(dirname(__file__), '.env')
# get the env file
load_dotenv(dotEnvPath) 

# function that sends the data to the sql server.
def SqlSend(data):
    # this gets the data from .env and creates a connection to the sql server
    db = mysql.connector.connect(
        host = os.environ.get("host"),
        username = os.environ.get("sqlusername"),
        password = os.environ.get("password"),
        database = os.environ.get("database"),
        
    )
    # creates a cursor object to command, the buffer arguement avoids pulling multiple lines at once, as this creates errors
    mycursor = db.cursor(buffered=True)
    # insert command (note the ignore means that if data is in the db already, dont put it in there)
    sql = "INSERT IGNORE INTO movies (site, filmName) VALUES (%s, %s);"
    # create blank list
    dataFormat = []
    #ignores the key values, only puts the values into the sql insert
    for i in data.values():
        #add the values to a list
        dataFormat.append(i)
    # this is for when searching for the film later
    dataFormat[1] = dataFormat[1].lower()
    #sql to see if the film is already in the database
    sqlCheck = 'SELECT COUNT(*) from movies where filmName like "{filmName}" and site like "{site}" '.format(site=dataFormat[0],filmName=dataFormat[1])
    # execute a prior check to see if the data is in the database
    mycursor.execute(sqlCheck)
    # save the cursor text as a variable
    check = mycursor.fetchall()
    # if the count of the film in the db is 0 (not there) then insert it, otherwise skip it
    if (check[0][0] == 0):
        # send the insert request, along with the data that is now formatted to be sent
        mycursor.execute(sql, dataFormat)
        # commit the change
        db.commit()
        # flavour text
        print(dataFormat, " was inserted.")
    else:
        print(dataFormat[1], "Was found in table -- skipping")
    #close the connection
    mycursor.close()
    db.close()

# function that will be used to find a film in either the database.
def findFilm(filmTitle):
    # this gets the data from .env and creates a connection to the sql server
    db = mysql.connector.connect(
        host = os.environ.get("host"),
        username = os.environ.get("sqlusername"),
        password = os.environ.get("password"),
        database = os.environ.get("database")
    )
    #create a cursor
    mycursor = db.cursor()
    # data validation for making sure the correct kind of data is put in
    if (str(filmTitle)):
        filmTitle = filmTitle.lower()
        # sql query to find data on film
        sql = 'SELECT * FROM movies WHERE filmName LIKE "{filmName}";'.format(filmName=filmTitle)
        # run the query
        mycursor.execute(sql)
        # save return text to parse to user
        returnText = mycursor.fetchall()
        # example of return data 
        # comes back as a list with a tuple inside, can then ignore the id and just return the platform and film title to the user
        # [(11800, 'Prime video', 'ted')]
        if(len(returnText) > 0):
            # log to console
            film = returnText
            return film

        else:
            # return that the film cant be found and that the user should try again tommorrow. 
            print("Film Not found")
            return None
    else:
        # return an error
        print("Bad Request")
        return None

# get films by site
def findFilmsOfSite(site):
    # this gets the data from .env and creates a connection to the sql server
    db = mysql.connector.connect(
        host = os.environ.get("host"),
        username = os.environ.get("sqlusername"),
        password = os.environ.get("password"),
        database = os.environ.get("database")
    )
    #create a cursor
    mycursor = db.cursor()
    # data validation for making sure the correct kind of data is put in
    if (str(site)):
        # sql query to find data on film
        sql = 'SELECT * FROM movies WHERE site like "{site}";'.format(site=site)
        # run the query
        mycursor.execute(sql)
        # save return text to parse to user
        returnText = mycursor.fetchall()
        # example of return data 
        # comes back as a list with a tuple inside, can then ignore the id and just return the platform and film title to the user
        # [(11800, 'Prime video', 'ted')]
        if(len(returnText) > 0):
            # log to console
            print(returnText)
            # convert to json obj
            filmJsonObject = json.dumps(returnText)
        else:
            print("Films Not found")
            # return that the film cant be found and that the user should try again tommorrow. 
    else:
        # return an error
        print("Bad Request")
    return filmJsonObject

# this function is going to be incharge of getting rid of films no longer in the database, aswell as rescrapes, to use this just plug the old list in to compare
def pruneOldFilms(oldList):
    # initally rescrape the sites
    newList = scraperManager()
    # compare the items in both
    for item in newList:
        if (item in oldList):
            print("{item} still in database".format(item=item))
        else:
            print("{item} not in database, pruning".format(item=item))
            
            # this gets the data from .env and creates a connection to the sql server
            db = mysql.connector.connect(
                host = os.environ.get("host"),
                username = os.environ.get("sqlusername"),
                password = os.environ.get("password"),
                database = os.environ.get("database")
            )
            #create a cursor
            mycursor = db.cursor()
            # due to dictionary items not being subscriptable i have to convert it to a list
            formattedData = []
            # for each item in the values of the dictionary
            for i in item.values():
                # add to a list
                formattedData.append(i)
            # delete old movie from database query
            sql = 'DELETE FROM movies WHERE filmName like "{filmName}" and site like "{site}"'.format(filmName=formattedData[1].lower(), site=formattedData[0])
            # try command
            try:
                # execute the query
                mycursor.execute(sql)
                # print result
                print("Deleted!")
            except Exception as err:
                # print the error
                print(err)
            # commit the change
            db.commit()
            # close connections
            mycursor.close()
            db.close()

# function that gets the films from the scraper script, then puts them into sql db
def scraperManager():
    print("-- Scraping Sites --")
    # blank list
    movies = []
    # initial scrapes to populate sql tables
    try:
        # this will attempt to get these three functions to scrape
        primeList = moviePuller.getPrimeFilms()
        nowList = moviePuller.getNowTVFilms()
        all4List = moviePuller.getAll4Films()
        
    except Exception as err:
        # just print the issue to the console and continue with the other scrapes
        print(err)
    
    # this line checks if the variable exists, we use this to manage which functions sucessfully called - as they will only exist if they pass
    if 'primeList' in locals():
        # for each element in the list, turn it into a dictionary
        for i in primeList:
            mov = {
                "site" : "Prime video",
                "film name" : i
            }
            # append it to the list
            movies.append(mov)
    else:
        # TODO schedule a rescrape if this doesnt work
        print("Prime video Scrape X")
    
    if 'nowList' in locals():
        for i in nowList:
            mov = {
                "site" : "Now TV",
                "film name" : i
            }
            movies.append(mov)
    else:
        print("Now TV Scrape X")

    if 'all4List' in locals():
        for i in all4List:
            mov = {
                "site" : "All4",
                "film name" : i
            }
            movies.append(mov)
    else:
        print("All4 Scrape X")

    # for each movie in the list
    for item in movies:
        try:
            # try to send the film to the sql db
            SqlSend(item)
        except Exception as err:
            # else just print the error
            print("error : ", err)
            break
    # for pruning
    return movies

start = time.perf_counter()
# initial scrape function call when api starts up
oldList = scraperManager()
finish = time.perf_counter()
# nice little performance monitor with green text colour
print("\033[1;32m Time taken = {time} seconds".format(time=round(finish-start)))
print("Starting Flask")
# API SECTION
# create app
app = Flask(__name__)
# needed for access control allow origin issue in js
CORS(app)
# scheduler for daily rescrapes
# initialize the scheduler
scheduler = BackgroundScheduler()
# schedule a prune everyday at 10pm to referesh the database
# a cron is a unix job scheduler command line utility - very useful for servers and very useful for my project
scheduler.add_job(func=pruneOldFilms, args=[oldList], trigger="cron", hour="22")
# start the scheduler
scheduler.start()

# shutdown function
def schedulerShutdown(signum, frame):
    print("Shutting down")
    scheduler.shutdown(wait=False)
    exit(1)

# interface for the sql database to the client, will do things such as request rescrapes for missing films - and returning film data to the client
# default path for the api
@app.route("/")
def default():
    # perhaps return all films?
    return "<p> this is default route nerd - try /prime or something</p>"

# api route for finding a film in the database
@app.route("/findFilm", methods=["GET"])
def filmRequest():
    # if the request method is GET
    if request.method == "GET":
        # payload of the request
        y = request.get_json()
        # we store the request to the filmname
        filmName = y["filmName"]
    
    x = findFilm(filmName)  
    return jsonify(x)

# api route to return all films from each site 
@app.route("/prime")
def postPrime():
    prime = findFilmsOfSite("Prime video")
    return prime

@app.route("/now")
def postNow():
    now = findFilmsOfSite("Now TV")
    return now

@app.route("/all")
def postAll4():
    all4 = findFilmsOfSite("all4")
    return all4

# start app
if __name__ == '__main__':
    app.run(host='0.0.0.0')

# catch ctrl c to exit
signal.signal(signal.SIGINT, schedulerShutdown)

