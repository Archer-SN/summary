function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener("DOMContentLoaded", () => {
    const listContainer = document.getElementById("list-container");
    const searchBar = document.getElementById("search");
    const sortSelect = document.getElementById("sort");
    const categorySelect = document.getElementById("category-filter");
    const urlDivs = document.getElementsByClassName("url");
    const favoriteButtons = document.getElementsByClassName("favorite");

    const showReadingButton = document.getElementById("show-reading-btn");
    if (document.contains(showReadingButton)){
        showReadingButton.addEventListener("click", () => {
            handleActiveButtons("show-reading-btn");
            handleContainers("reading");
            
        });
    }

    const showFinishedButton = document.getElementById("show-finished-btn");
    if (document.contains(showFinishedButton)) {
        showFinishedButton.addEventListener("click", () => {
            handleActiveButtons("show-finished-btn");
            handleContainers("finished");

        });
    }
        
    const showFavoriteButton = document.getElementById("show-favorite-btn");
    if (document.contains(showFavoriteButton)) {
        showFavoriteButton.addEventListener("click", () => {
            handleActiveButtons("show-favorite-btn");
            handleContainers("favorites");
        });
    }

    const readingButtons = document.getElementsByClassName("reading-btn");
    const finishedButtons = document.getElementsByClassName("finished-btn");
    const removeButtons = document.getElementsByClassName("remove-btn");

    for (let i = 0; i < readingButtons.length; i++) {
        readingButtons[i].addEventListener("click", handleReading)
    }
    
    for (let i = 0; i < finishedButtons.length; i++) {
        finishedButtons[i].addEventListener("click", handleFinished)
    }

    for (let i = 0; i < removeButtons.length; i++) {
        removeButtons[i].addEventListener("click", handleRemove)
    }

    if (document.contains(searchBar)){
        searchBar.addEventListener("input", () => getContent(listContainer));
    } 
    if (document.contains(sortSelect)) {
        sortSelect.addEventListener("change", () => getContent(listContainer));
    }
    if (document.contains(categorySelect)){
        categorySelect.addEventListener("change", () => getContent(listContainer));
    }

    for (let i = 0; i < urlDivs.length; i++) {
        urlDivs[i].addEventListener("click", redirect);
    }

    for (let i = 0; i < favoriteButtons.length; i++) {
        favoriteButtons[i].addEventListener("click", handleFavorite)
    }
})

function getContent(container) {
    const searchBar = document.getElementById("search");
    const sortSelect = document.getElementById("sort");
    const categorySelect = document.getElementById("category-filter");

    const contentType = container.dataset.contentType;
    const fetchUrl = contentType == "book" ? "/books" : "/articles";
    fetch(`${fetchUrl}?search=${searchBar.value}&sort=${sortSelect.value}&category=${categorySelect.value}`)
    .then(response => response.json())
    .then(data => {
        container.replaceChildren();
        if (data.content_list.length == 0) {
            container.textContent = `No ${contentType} for now ..`;
        }
        for (let i = 0; i < data.content_list.length; i++) {
            container.append(createCard(contentType, data.content_list[i]));
        }
    })
    .catch(error => console.log(error))
}


function createCard(contentType, content) {
    // contentLink is the true container
    const contentContainer = document.querySelector("#template").cloneNode(true);
    contentContainer.dataset.contentType = contentType;
    contentContainer.dataset.contentId = content.id;
    contentContainer.classList.remove("d-none");
    const urlDivs = contentContainer.getElementsByClassName("url");
    for (let i = 0; i < urlDivs.length; i++) {
        urlDivs[i].addEventListener("click", redirect)
    }
    const thumbnail = contentContainer.querySelector(".thumbnail");
    thumbnail.setAttribute("src", content.thumbnail);
    const category = contentContainer.querySelector(".category");
    category.textContent = content.category;
    const title = contentContainer.querySelector(".title");
    title.textContent = content.title;
    const bookAuthor = contentContainer.querySelector(".book-author");
    if (typeof(bookAuthor) != 'undefined' && bookAuthor != null) {
        bookAuthor.textContent = `By ${content.book_author}`;
        bookAuthor.setAttribute("href", `user/${content.book_author}`)
    }
    const authorPrefix = contentContainer.querySelector(".author-prefix");
    if (contentType === "book") {
        authorPrefix.textContent = "Summarized by ";
    }
    else {
        authorPrefix.textContent = "Created by ";
    }
    const author = document.createElement("a");
    author.setAttribute("href", `/user/${content.author}`);
    author.textContent = content.author
    authorPrefix.append(author);
    const dateCreated = contentContainer.querySelector(".date-created");
    dateCreated.textContent = `Created ${content.date_created}`;

    const bottomBox = contentContainer.querySelector(".bottom-box");
    bottomBox.dataset.contentType = contentType;
    bottomBox.dataset.contentId = content.id;

    const favoriteButton = contentContainer.querySelector(".favorite");
    favoriteButton.addEventListener("click", handleFavorite);

    if (content.favorite) {
        favoriteButton.classList.remove("not-favorite");
        favoriteButton.classList.add("is-favorite");
    } else {
        favoriteButton.classList.remove("is-favorite");
        favoriteButton.classList.add("not-favorite");
    }

    return contentContainer;
}


function redirect() {
    location.href=`${this.parentNode.dataset.contentType}s/${this.parentNode.dataset.contentId}`;
}

function handleContainers(id) {
    const bookContainers = document.getElementsByClassName("book-container");
    for (let i = 0; i < bookContainers.length; i++) {
        if (bookContainers[i].getAttribute("id") == id) {
            bookContainers[i].classList.add("d-flex");
            bookContainers[i].classList.remove("d-none");
        } else {
            bookContainers[i].classList.add("d-none");
            bookContainers[i].classList.remove("d-flex");
        }
    }
}

function handleActiveButtons(id) {
    const showButtons = document.getElementsByClassName("show-btn");
    for (let i = 0; i < showButtons.length; i++) {
        if (showButtons[i].getAttribute("id") == id) {
            showButtons[i].classList.add("border-bottom", "border-3", "fw-bold");
        } else {
            showButtons[i].classList.remove("border-bottom", "border-3", "fw-bold");
        }
    }
}


function handleFavorite() {
    const parent = this.parentNode;
    const card = parent.parentNode;
    fetch(`${parent.dataset.contentType}s/${parent.dataset.contentId}`, {
        method: "PUT",
        body: JSON.stringify({"action": "favorite"}), 
        headers: {"X-CSRFToken": csrftoken, 'Content-Type': 'application/json'},
        mode: "same-origin" // Do not send CSRF token to another domain.
    })
    .then(response => response.json())
    .then(data => {
        if (data.className == "is-favorite") {
            this.classList.remove("not-favorite")
            this.classList.add(data.className)
            // favorite all related cards
            if (parent.dataset.contentType == "book") {
                // Favorite all related cards
                const relatedCards = document.querySelectorAll(`[data-content-id~='${parent.dataset.contentId}']`)
                const favoriteContainer = document.getElementById("favorites");
                for (let i = 0; i < relatedCards.length; i++) {
                    const relatedStar = relatedCards[i].querySelector(".favorite");
                    relatedStar.classList.remove("not-favorite")
                    relatedStar.classList.add("is-favorite")
                }
                if (favoriteContainer != null && favoriteContainer.querySelector(`[data-content-id='${parent.dataset.contentId}']`) == null) {
                    if (favoriteContainer.firstElementChild.tagName == "P") {
                        favoriteContainer.replaceChildren();
                    }
                    // If the card is favorited then it should have at least 1 card to copy
                    const cardClone = relatedCards[0].cloneNode(true);
                    const urlDivs = cardClone.getElementsByClassName("url");
                    for (let i = 0; i < urlDivs.length; i++) {
                        urlDivs[i].addEventListener("click", redirect)
                    }
                    cardClone.querySelector(".favorite").addEventListener("click", handleFavorite);
                    if (cardClone.contains(cardClone.querySelector("ul")) == false) {
                        createDropdown(cardClone);
                    }
                    const readingButton = document.createElement("li");
                    readingButton.className = "dropdown-item reading-btn"
                    readingButton.textContent = "Move to Currently Reading"
                    readingButton.addEventListener("click", handleReading);
                    cardClone.querySelector("ul").replaceChildren()
                    cardClone.querySelector("ul").append(readingButton);
                    favoriteContainer.append(cardClone);
                }
            }
        } else {
            this.classList.remove("is-favorite")
            this.classList.add(data.className)
            if (parent.dataset.contentType == "book") {
                // Unfavorite all related cards
                const relatedCards = document.querySelectorAll(`[data-content-id~='${parent.dataset.contentId}']`)
                for (let i = 0; i < relatedCards.length; i++) {
                    const relatedStar = relatedCards[i].querySelector(".favorite");
                    relatedStar.classList.remove("is-favorite")
                    relatedStar.classList.add("not-favorite")
                }
            }
        }
    })
}

function handleReading() {
    const dropdown = this.parentNode;
    const dropdownParent = dropdown.parentNode;
    const card = dropdownParent.parentNode;
    const cardContainer = card.parentNode;
    const readingContainer= document.getElementById("reading");
    const finishedContainer = document.getElementById("finished");
    fetch(`books/${dropdownParent.dataset.contentId}`, {
        method: "PUT",
        body: JSON.stringify({"action": "reading"}), 
        headers: {"X-CSRFToken": csrftoken, 'Content-Type': 'application/json'},
        mode: "same-origin" // Do not send CSRF token to another domain.
    })
    .then(response => {
        if (response.status == 201) {
            const finishedButton = document.createElement("li");
            finishedButton.className = "dropdown-item finished-btn";
            finishedButton.textContent = "Move to Finished"
            finishedButton.addEventListener("click", handleFinished);
            const removeButton = document.createElement("li");
            removeButton.className = "dropdown-item remove-btn"
            removeButton.textContent = "Remove from Home"
            removeButton.addEventListener("click", handleRemove);

            if (readingContainer.firstElementChild.tagName == "P") {
                readingContainer.replaceChildren();
            }

            if (cardContainer.getAttribute("id") == "favorites") {
                const cardClone = card.cloneNode(true);
                const urlDivs = cardClone.getElementsByClassName("url");
                for (let i = 0; i < urlDivs.length; i++) {
                    urlDivs[i].addEventListener("click", redirect)
                }
                const cloneDropdown = cardClone.querySelector(".dropdown-menu");
                cardClone.querySelector(".favorite").addEventListener("click", handleFavorite);
                cloneDropdown.replaceChildren()
                cloneDropdown.append(finishedButton, removeButton)
                readingContainer.appendChild(cardClone);
                finishedContainer.removeChild(finishedContainer.querySelector(`[data-content-id='${cardClone.dataset.contentId}']`))
            } else {
                readingContainer.appendChild(card);
                dropdown.replaceChildren();
                dropdown.append(finishedButton, removeButton)
            }   
            
            // Favorite books won't get removed when moved so we don't have to worry about it now
            addEmptyText()
        }
    })
    .catch(error => console.log(error))
} 

function handleFinished() {
    const dropdown = this.parentNode;
    const dropdownParent = dropdown.parentNode;
    const card = dropdownParent.parentNode;
    const cardContainer = card.parentNode;
    const finishedContainer = document.getElementById("finished");
    fetch(`books/${dropdownParent.dataset.contentId}`, {
        method: "PUT",
        body: JSON.stringify({"action": "finished"}), 
        headers: {"X-CSRFToken": csrftoken, 'Content-Type': 'application/json'},
        mode: "same-origin" // Do not send CSRF token to another domain.
    })
    .then(response => {
        const readingButton = document.createElement("li");
        readingButton.className = "dropdown-item reading-btn"
        readingButton.textContent = "Move to Currently Reading"
        readingButton.addEventListener("click", handleReading);
        const removeButton = document.createElement("li");
        removeButton.className = "dropdown-item remove-btn"
        removeButton.textContent = "Remove from Home"
        removeButton.addEventListener("click", handleRemove)

        if (finishedContainer.firstElementChild.tagName == "P") {
            finishedContainer.replaceChildren();
        }
        finishedContainer.appendChild(card);
        dropdown.replaceChildren();
        dropdown.append(readingButton, removeButton)

        addEmptyText()
    })
    .catch(error => console.log(error))
}


function handleRemove() {
    const dropdown = this.parentNode;
    const dropdownParent = dropdown.parentNode;
    const card = dropdownParent.parentNode;
    const contentId = card.dataset.contentId;
    const cardContainer = card.parentNode;
    const cardContainerId = cardContainer.getAttribute("id")
    const from = cardContainerId == "favorites" ? "favorites" : cardContainerId == "finished" ? "finished" : "reading"
    fetch(`books/${dropdownParent.dataset.contentId}`, {
        method: "PUT",
        body: JSON.stringify({"action": "remove", "from": from}), 
        headers: {"X-CSRFToken": csrftoken, 'Content-Type': 'application/json'},
        mode: "same-origin" // Do not send CSRF token to another domain.
    })
    .then(response => {
        // Removing the card
        card.remove()
        addEmptyText()
    })
}   

function createDropdown(card) {
    const icon = document.createElement("i");
    icon.className = "options dropdown-toggle fa-solid fa-ellipsis-vertical mt-1"
    icon.setAttribute("role", "button")
    icon.setAttribute("data-bs-toggle", "dropdown")
    icon.setAttribute("aria-expanded", "false")
    const ul = document.createElement("ul");
    ul.className = "mt-3 dropdown-menu dropdown-menu-lg-end user-select-none"
    card.querySelector(".bottom-box").append(icon, ul);
}

function addEmptyText() {
    const readingContainer = document.getElementById("reading");
    const finishedContainer = document.getElementById("finished");
    const favoriteContainer = document.getElementById("favorites");
    if (readingContainer.children.length == 0) {
        const emptyContainerText = document.createElement("p");
        emptyContainerText.innerHTML = "No reading book. You can find books <a href='/books'>here</a>"
        readingContainer.append(emptyContainerText);
    }
    if (finishedContainer.children.length == 0) {
        const emptyContainerText = document.createElement("p");
        emptyContainerText.innerHTML = "No finished book. You can find books <a href='/books'>here</a>"
        finishedContainer.append(emptyContainerText);
    }
    if (favoriteContainer.children.length == 0) {
        const emptyContainerText = document.createElement("p");
        emptyContainerText.innerHTML = "No favorite book. You can find books <a href='/books'>here</a>"
        finishedContainer.append(emptyContainerText);
    }
}