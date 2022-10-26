![](🎥_Movie_DataBase_🎞️.png)
![GitHub language count](https://img.shields.io/github/languages/count/s-riches/moviedatabase) ![GitHub repo size](https://img.shields.io/github/repo-size/s-riches/moviedatabase)

#### Visual Example :

![MovieDB in action](movieDB.gif)

#### Summary

Recently i created an API using .NET along with Docker and a few other pieces of technology at some work experience - since then i have had a huge interest in combining different parts of my knowledge into a full stack program, but due to my college course i had spent a lot of time away from programming. Therefore i present my first attempt at an independent full stack application : **MovieDB**.

Using python along with flask for the backend and some different libraries i wrote a few scripts to scrape different streaming websites that i use personally to tell me what is available for me to watch. For the frontend i used bootstrap along with vanilla javascript to present a nice interface. I will also be using MySQL server to store information to cut down on computing power needed, as the scraping should only need to happen once a day at most.

The basic flow of the program works like this, the client makes a request to the api to find a movie they want to watch, the api checks the database to see if the movie is in there, if so it returns all the data needed. The api should also be able to return all of the movies by website if requested, and rescrape daily to keep the database current.

#### Libraries used:

-   Flask
-   Requests
-   Requests-html
-   Dotenv
-   mysql.connector
-   os (obviously)
-   time (for performance monitoring)
-   signal (needed for program control)
-   json (for formatting)
-   APScheduler

### Setup

-   Prior to trying to run this project, you need to install python and docker
-   clone the image into a folder
-   Firstly run the init (located in the scraper_scripts folder) file in a terminal, or simply click on the init file
-   Enter a password to set as your Database password
-   Go to your terminal and navigate to the the cloned folder.
-   Type `docker-compose up`
-   then go to the frontend folder and open the index html file in your browser.
-   after that the program should be working as intended!
-   to close the docker containers type `docker-compose down`
-   to remove the persistent data instead type `docker-compose down -v`
