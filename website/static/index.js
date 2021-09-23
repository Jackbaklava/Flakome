"use strict";

function redirect(url) {
    window.location.href = url;
}


function deletePost(postId) {
    fetch("/delete-post", {
        method: "POST",
        body: JSON.stringify({postId: postId})
    })
    .then(res => {
        redirect("/")
    })
}
