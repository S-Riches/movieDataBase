// create a class for a card to display on the page
class Card {
  constructor(title, site) {
    this.title = title;
    this.site = site;
  }
}
// make calls to the api to get the data needed for the cards - can just change the site to get different sites
async function getFilms(site) {
  let response = await fetch(`http://127.0.0.1:5000/${site}`);
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
  // find the outbox row, checks if the number is divisable by three to ensure three to a row
  if (boxId < 3){
    const location = document.getElementById('outBox');
    location.appendChild(newEl)
  }
  else if (boxId % 3 === 0) {
    const location = document.getElementById(`outBox${boxId}`);
    // insert it
    location.appendChild(newEl);
  }
}
// create a row containing three cards
function createRow(list) {
  // count to three - duh
  var counter = 0;
  for (let i = 0; i < list.length; i++) {
    // create the card
    console.log(boxId)
    createCard(list[i][1], list[i][0], boxId);
    counter++;
    if (counter === 3) {
      // create new outbox
      const div = document.createElement("div");
      div.className += "row";
      div.id += `outBox${i + 1}`;
      // store the value to be accessed in the create card method
      var boxId = i + 1;
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
    let response = await fetch(`http://127.0.0.1:5000/findFilm`, {
      method: "POST",
      mode: "cors",
      headers: { "Content-Type": " application/json;charset=UTF-8" },
      body: JSON.stringify({ filmName: title }),
    });
    return response.json();
  }
  function filmQuery() {
    // only execute if the data isnt null
    if (document.getElementById("movieQuery").value != "") {
      let movieQuery = document.getElementById("movieQuery").value;
      // .then means that we fufill the promise and therefore have to do something with the data once we get it
      searchFilm(movieQuery).then((response) => {
        createRow(response)
      });
    }
  }
} else {
  // card creation
  getFilms(searchName).then((data) => {
    // create a var called list from the returned data
    createRow(data);
  });
}
