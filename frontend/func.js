// create a class for a card to display on the page
class Card{
    constructor(title, site){
        this.title = title;
        this.site = site;
    }
}
// make calls to the api to get the data needed for the cards - can just change the site to get different sites
async function getFilms(site){
    let response = await fetch(`http://127.0.0.1:5000/${site}`);
    let data = await response.json();
    return data;
}

// also create the search function to look for a specific movie and then another for looking for a movie in a list
async function searchFilm(title){
    // research how to add headers to fetch
    let response = await fetch(`http://127.0.0.1:5000`);
}

// function to create a card
function createCard(title, site, boxId){
    //make the first letter upper case
    var newTitle = String(title).charAt(0).toUpperCase() + String(title).slice(1);
    // create a card class
    var card = new Card(newTitle, site);
    // create a new element
    const newEl = document.createElement("div");
    newEl.className += "d-flex justify-content-center text-center col card bg-dark text-light";
    newEl.id += "card";
    // create a title
    const titleContent = document.createElement("h4");
    // set the text correctly
    titleContent.innerText = card.title;
    // styling
    titleContent.className += "card-title";
    const siteContent = document.createElement("p");
    siteContent.innerText = card.site;
    siteContent.className += "card-subtitle"
    // append the div with the text
    newEl.appendChild(titleContent);
    newEl.appendChild(siteContent);
    // find the outbox
    if((boxId % 3) === 0){
        const location = document.getElementById(`outBox${boxId}`);
        // insert it
        location.appendChild(newEl);
    }
    else{
        const location = document.getElementById("outBox");
        // insert it
        location.appendChild(newEl);
    }
}
// create a row containing three cards
function createRow(list){
    // count to three - duh
    var counter = 0;
    for(let i = 0; i < list.length; i++){
        // create the card
        createCard(list[i][1], list[i][0], boxId);
        counter++;
        if(counter === 3){
            // create new outbox
            const div = document.createElement("div");
            div.className += "row";
            div.id += `outBox${i+1}`;
            // store the value to be accessed in the create card method
            var boxId = i+1;
            const outBox = document.getElementById("outBox")
            document.getElementById("outBoxDiv").insertBefore(div,outBox);
            counter = 0;
        }
    }
}

// find what page we are on
var page = window.location.pathname.substring(window.location.pathname.lastIndexOf("/"));
//console.log(page);
if(page === "/all.html"){
    // card creation
    getFilms('all').then(data => {
        // create a var called list from the returned data
        var list = data;
        createRow(list)
    });
}
if(page === "/now.html"){
    // card creation
    getFilms('now').then(data => {
        // create a var called list from the returned data
        var list = data;
        createRow(list)
    });
}
if(page === "/prime.html"){
    // card creation
    getFilms('prime').then(data => {
        // create a var called list from the returned data
        var list = data;
        createRow(list)
    });
}
if(page === "/index.html"){
    // search funtion code goes here
    /*
        basic idea for this is to do:
        - wait for user to press search button
            - add a listener to check when the button is pressed
            - take the inner text in the input and run it through data validation
        - do data validation to ensure that the title is actually a string, isnt sql code, etc
            - convert to lower case as thats how its stored
            - research this to find a good method or some other way of sanitizing the input
        - send the request using the find film function
            - need to research a way to add headers to the find film function
            - format the string to allow for the search to work
            - make sure that there is a good response, if not prompt the user to try again
        - return the film into the box
            - just use the function already created
    */
}

