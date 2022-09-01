#imports
#from threading import Thread
import moviePuller
from flask import Flask
from dotenv import load_dotenv
import os
import mysql.connector
from os.path import join, dirname

# perhaps the script should first scrape the websites, then start the flask app to get that data into the sql table and retrieve whats needed, then we can schedule when to rescrape.
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
    # creates a cursor object to command
    mycursor = db.cursor()
    # insert command
    sql = "INSERT INTO movies (site, filmName) VALUES (%s, %s);"
    # create blank list
    dataFormat = []
    #ignores the key values, only puts the values into the sql insert
    for i in data.values():
        #add the values to a list
        dataFormat.append(i)
    # send the insert request, along with the data that is now formatted to be sent
    mycursor.execute(sql, dataFormat)
    # commit the change
    db.commit()
    # flavour text
    print(mycursor, " was inserted.")
    #close the connection
    db.close()

# script that gets the films from the scraper script, then puts them into sql db
def addFilms():
    #TODO need to check if the film already exists in the db, if so skip it and check the next one - then remove if its not in the current list. this will stop duplication of data
    # blank list
    movies = []
    # initial scrapes to populate sql tables
    # TODO make these scrape all at the same time. - possibly with threading as it will make this faster
    try:
        primeList = moviePuller.getPrimeFilms()
        nowList = moviePuller.getNowTVFilms()
        all4List = moviePuller.getAll4Films()
    except Exception:
        # just print the issue to the console and continue with the other scrapes
        print(Exception)
        pass
        
    # for each element in the list, turn it into a dictionary
    for i in primeList:
        mov = {
            "site" : "Prime video",
            "film name" : i
        }
        # append it to the list
        movies.append(mov)
    for i in nowList:
        mov = {
            "site" : "Now TV",
            "film name" : i
        }
        movies.append(mov)
    for i in all4List:
        mov = {
            "site" : "All4",
            "film name" : i
        }
        movies.append(mov)

    # update table if film isnt in there,
    try:
        # try to send the film to the sql db
        for item in movies:
            SqlSend(item)
    except:
        print("Film already exists")
        pass


addFilms()

#API SECTION

# this will function as the api doing the managing for the scraping calls, it will also handle the sql database and will be able to be interfaced via flask.
app = Flask(__name__)

# default path for the api
@app.route("/")
def default():
    return "<p> this is default route nerd - try /prime or something</p>"

# these paths will come back with sql data.
@app.route("/prime")
def postPrime():
    return "<p> list = {list} </p>".format(list = primeMovies)
@app.route("/now")
def postNow():
    pass
@app.route("/all")
def postAll4():
    pass
