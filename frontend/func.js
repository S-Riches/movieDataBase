// create a class for a card to display on the page
class Card {
  constructor(title, site) {
    this.title = title;
    this.site = site;
  }
}
// make calls to the api to get the data needed for the cards - can just change the site to get different sites
async function getFilms(site) {
  let response = await fetch(`http://127.0.0.1:5001/${site}`);
  let data = await response.json();
  return data;
}

// function to create a card
function createCard(title, site, boxId) {
  //make the first letter upper case
  var newTitle = String(title).charAt(0).toUpperCase() + String(title).slice(1);
  // create a card class
  var card = new Card(newTitle, site);
  // create a new element
  const newEl = document.createElement("div");
  // bootstrap code
  newEl.className +=
    "d-flex justify-content-center text-center col card bg-dark text-light";
  // create a title and site
  const titleContent = document.createElement("h4");
  const siteContent = document.createElement("p");
  // set the text correctly
  titleContent.innerText = card.title;
  siteContent.innerText = card.site;
  // styling with bootstrap
  titleContent.className += "card-title";
  siteContent.className += "card-subtitle";
  // append the div with the text
  newEl.appendChild(titleContent);
  newEl.appendChild(siteContent);
  // find the outbox row, checks if the number is divisible by three to ensure three to a row
  if (boxId % 3 === 0) {
    const location = document.getElementById(`outBox${boxId}`);
    // insert it
    location.appendChild(newEl);
  }
}
// create a row containing three cards
function createRows(list) {
  // count to three - duh
  let counter = 0;
  let boxId = 0;
  for (let i = 0; i < list.length; i++) {
    // create the card
    createCard(list[i][1], list[i][0], boxId);
    counter++;
    if (counter === 3) {
      // create new outbox
      boxId += 3;
      const div = document.createElement("div");
      div.className += "row";
      div.id += `outBox${boxId}`;
      // store the value to be accessed in the create card method
      const outBox = document.getElementById("outBox");
      document.getElementById("outBoxDiv").insertBefore(div, outBox);
      counter = 0;
    }
  }
}

// find what page we are on
const page = window.location.pathname.substring(
  window.location.pathname.lastIndexOf("/")
);
// format the search name for the get films method to work
const searchName = page
  .substring(page.indexOf("/"), page.indexOf("."))
  .slice(1);

// check if the user selected the search page
if (searchName === "index") {
  // also create the search function to look for a specific movie and then another for looking for a movie in a list
  async function searchFilm(title) {
    // create a request to the api which uses post and contains a body
    let response = await fetch(`http://127.0.0.1:5001/findFilm`, {
      method: "POST",
      mode: "cors",
      headers: { "Content-Type": " application/json;charset=UTF-8" },
      body: JSON.stringify({ filmName: title }),
    });
    return response.json();
  }
  function filmQuery() {
    // only execute if the data isn't null
    if (document.getElementById("movieQuery").value != "") {
      let movieQuery = document.getElementById("movieQuery").value;
      // .then means that we fulfill the promise and therefore have to do something with the data once we get it
      searchFilm(movieQuery).then((response) => {
        // check if the response yields anything - i.e. if it found a film
        if (response != null) {
          // get the element
          let outbox = document.getElementById("outBox0");   
          // if there are already children in the outbox
          if (outbox.childElementCount > 0){
            // while there are still children under the parent node
            while(outbox.firstChild){
              // delete the child
              outbox.removeChild(outbox.firstChild);
            }
          }
          for (let i = 0; i < response.length; i++) {
            createCard(response[i][1], response[i][0], 0);
          }
        } else {
          // if not found send alert to user
          alert("Movie not found in database, try again tomorrow!");
        }
      });
    }
  }
} else {
  // card creation
  getFilms(searchName).then((data) => {
    // create a var called list from the returned data
    createRows(data);
  });
}
