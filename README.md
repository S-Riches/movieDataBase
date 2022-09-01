# Movie DataBase

Recently i created an API using .NET along with Docker and a few other pieces of technology at some work experience - since then i have had a huge interest in combining different parts of my knowledge into a full stack program, but due to my college course i had spent alot of time away from programming. Therefore i present my first attempt at an independent full stack application : **MovieDB**.

Using python along with flask for the backend and some different libraries i will be writing a few scripts to scrape different streaming websites that i use personally to tell me what is available for me to watch. For the frontend i will be using bootstrap along with vanilla javascript(undecided possibly could use react incase i want to make the interface more pretty) to present a nice interface. I will also be using MySQL server to store information to cut down on computing power needed, as the scraping should only need to happen once a day at most.

The basic flow of the program should work like this, the client makes a request to the api to find a movie they want to watch, the api checks the database to see if the movie is in there, if so it returns all the data needed, if not then it scrapes the websites again - updates the database by deleting the movies no longer available and adding the new ones only, and if it cant find it after that itll return saying that the movie isnt available on these services.

Once the project is done i will include the full list of libraries used within python, but at the moment we have:
- Flask
- Requests
- Requests-html
- Dotenv
- mysql-connector
- os (obviously)


I will also make a focus to use Docker to make my program more portable incase i ever want to show someone it.
