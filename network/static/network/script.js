// Form submission
// Make sure that the form submits a new post to the top of the load_posts view
// when it is submitted by the user
const postForm = document.getElementById('post-form');
postForm.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(postForm);
    fetch('/new_post', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'Post created successfully!') {
                const postList = document.getElementById('post-list');
                const postItem = document.createElement('div');
                postItem.className = 'post-item';
                postItem.innerHTML = `
                    <p><strong>${data.post.user}</strong></p>
                    <p>${data.post.body}</p>
                    <p>${data.post.timestamp}</p>
                    <p>Liked by: ${data.post.liked_by.join(', ')}</p>
                    <p>Comments: ${data.post.comments}</p>
                `;
                postList.insertBefore(postItem, postList.firstChild);
            }
            console.log("Post has been submitted");
            const textarea = document.getElementById('post-content');
            textarea.value = '';
        });
}); 

// Function to fetch and display all posts from server
const postsUrl = '/get_posts';
function fetchAndDisplayPosts() {
    fetch(postsUrl)
        .then(response => response.json())
        .then(data => {
            const postList = document.getElementById('post-list');

            data.posts.forEach(post => {
                const postItem = document.createElement('div');
                postItem.className = 'post-item';
                postItem.innerHTML = `
                    <p><strong>${post.author}</strong></p>
                    <p>${post.text}</p>
                    <p>${post.timestamp}</p>
                    <p>Liked by: ${post.liked_by.join(', ')}</p>
                    <p>Comments: ${post.comments.length}</p>
                `;
                postList.appendChild(postItem);
            });

            // Add pagination controls if needed
            // You can check data.num_pages, data.page, data.has_next, and data.has_previous
        })
        .catch(error => {
            console.error('Error fetching and displaying posts:', error);
        });
}

fetchAndDisplayPosts();