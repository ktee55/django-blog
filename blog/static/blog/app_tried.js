
fetch('/posts/api/')
.then(data => data.text())
.then(data => {
    // console.log(data); 
    const post_template = Handlebars.compile(document.querySelector('#post').innerHTML);
    // console.log(post_template);
    const post = post_template(data);
    document.querySelector('#handlebar-post').innerHTML = post
    
})



    // fetch('/post/{{post.id}}/comment/create')
    // .then(data => data.text())
    // .then(text => {
    //   const parser = new DOMParser();
    //   const htmlDocument = parser.parseFromString(text, "text/html");
    //   const section = htmlDocument.documentElement.querySelector("form");
    //   document.querySelector("#add_comment").appendChild(section);
    // })
    // fetch(url).then(data => data.text()).then(data => {
    //   document.querySelector(selector).innerHTML = data
    // }).then(completeCallback)


    
// // Infinite scroll

// // Start with first post.
// let counter = 1;

// // Load posts 20 at a time.
// const quantity = 5;

// // When DOM loads, render the first 20 posts.
// document.addEventListener('DOMContentLoaded', load);

// // If scrolled to bottom, load the next 20 posts.
// window.onscroll = () => {
//     if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
//         load();
//     }
// };


// // Load next set of posts.
// function load() {

//     // Set start and end post numbers, and update counter.
//     const start = counter;
//     const end = start + quantity - 1;
//     counter = end + 1;

//     // Open new request to get new posts.
//     const request = new XMLHttpRequest();
//     request.open('POST', '/posts/api/');
//     request.onload = () => {
//         const data = request.responseText;
//         console.log(data)
//         // data.forEach(add_post);
//     };

//     // Add start and end points to request data.
//     const data = new FormData();
//     data.append('start', start);
//     data.append('end', end);

//     // Send request.
//     const token = document.querySelector("[name=csrfmiddlewaretoken]").value;
//     // console.log(token);
//     request.setRequestHeader('Content-Type', token);
//     request.send(data);
// };

// // Add a new post with given contents to DOM.
// const post_template = Handlebars.compile(document.querySelector('#post').innerHTML);
// function add_post(contents) {

//     // Create new post.
//     const post = post_template({'contents': contents});

//     // Add post to DOM.
//     document.querySelector('#posts').innerHTML += post;

// }