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
    const favoriteButtons = document.getElementsByClassName("favorite");
    
    const commentButton = document.getElementById("comment-btn");

    if (!!commentButton) {
        commentButton.addEventListener("click", submitComment )
    }
    for (let i = 0; i < favoriteButtons.length; i++) {
        favoriteButtons[i].addEventListener("click", handleFavorite)
    }
})

function handleFavorite() {
    const parent = this.parentNode;

    fetch(`/${parent.dataset.contentType}s/${parent.dataset.contentId}`, {
        method: "PUT",
        body: JSON.stringify({"action": "favorite"}), 
        headers: {"X-CSRFToken": csrftoken, 'Content-Type': 'application/json'},
        mode: "same-origin" // Do not send CSRF token to another domain.
    })
    .then(response => response.json())
    .then(data => {
        if (data.className == "is-favorite") {
            this.classList.remove("not-favorite")
            this.classList.add("is-favorite")
        } else {
            this.classList.remove("is-favorite")
            this.classList.add("not-favorite")
        }
    })
}

function submitComment() {
    const commentForm = this.parentNode
    fetch("/comment", {
        method: "POST",
        body: JSON.stringify({"content_type": commentForm.dataset.contentType, "content_id": commentForm.dataset.contentId, "content": commentForm.querySelector("#comment-content").value}), 
        headers: {"X-CSRFToken": csrftoken, 'Content-Type': 'application/json'},
        mode: "same-origin" // Do not send CSRF token to another domain.
    })
    .then(response => {
        if (response.status == 201) {
            document.location.reload(true)
        }
    })
    .catch(error => console.log(error))
}