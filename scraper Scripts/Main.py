#imports
import moviePuller
from flask import Flask

# this script will function as the api doing the managing for the scraping calls, it will also handle the sql database and will be able to be interfaced via flask.
app = Flask(__name__)

# default path for the api
@app.route("/")
def default():
    return "<p> this is default route nerd - try /prime or something</p>"

# these paths will call the films and get them into a list.

@app.route("/prime")
def getPrime():
    # apparently python doesnt like this - so gonna have to learn scheduling and i SERIOUSLY need to make this async now lmao
    primeMovies = moviePuller.getPrimeFilms()
    return "<p>" + primeMovies +"</p>"

@app.route("/now")
def getNow():
    nowMovies = moviePuller.getNowTVFilms()

@app.route("/all")
def getAll4():
    all4Movies = moviePuller.getAll4Films()

