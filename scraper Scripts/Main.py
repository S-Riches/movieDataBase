#imports
#from threading import Thread
import string
import moviePuller
from flask import Flask
from dotenv import load_dotenv
import os
import mysql.connector
from os.path import join, dirname

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
        database = os.environ.get("database")
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
    #TODO MAKE SURE THAT THE SAME FILM ON ANOTHER SITE ALSO WORKS
    # this is for when searching for the film later
    dataFormat[1] = dataFormat[1].lower()
    #sql to see if the film is already in the database
    sqlCheck = 'SELECT COUNT(*) from movies where filmName like "{filmName}"'.format(filmName=dataFormat[1])
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
        pass
    #close the connection
    mycursor.close()
    db.close()

# function that will be used to find a film in either the database, or on a rescan.
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
        # log to console
        print(returnText)
    else:
        # return an error
        pass


# script that gets the films from the scraper script, then puts them into sql db
def scraperManager():
    # blank list
    movies = []
    # initial scrapes to populate sql tables
    # TODO make these scrape all at the same time. - possibly with threading as it will make this faster
    try:
        # this will attempt to get these three functions to scrape
        primeList = moviePuller.getPrimeFilms()
        nowList = moviePuller.getNowTVFilms()
        all4List = moviePuller.getAll4Films()
        pass
    except Exception as err:
        # just print the issue to the console and continue with the other scrapes
        print(err)
        pass

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
        pass
        
    if 'nowList' in locals():
        for i in nowList:
            mov = {
                "site" : "Now TV",
                "film name" : i
            }
            movies.append(mov)
    else:
        print("Now TV Scrape X")
        pass

    if 'all4List' in locals():
        for i in all4List:
            mov = {
                "site" : "All4",
                "film name" : i
            }
            movies.append(mov)
    else:
        print("All4 Scrape X")
        pass

    # for each movie in the list
    for item in movies:
        try:
            # try to send the film to the sql db
            SqlSend(item)
        except Exception as err:
            # else just print the error
            print("error : ", err)

# initial scrape function call when api starts up
scraperManager()
#API SECTION
# interface for the sql database to the client, will do things such as request rescrapes for missing films - and returning film data to the client

app = Flask(__name__)

# default path for the api
@app.route("/")
def default():
    return "<p> this is default route nerd - try /prime or something</p>"

# these paths will come back with sql data.
@app.route("/prime")
def postPrime():
    return "<p> list = {list} </p>".format(list = "x")
@app.route("/now")
def postNow():
    pass
@app.route("/all")
def postAll4():
    pass
