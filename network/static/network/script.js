// Fetch posts from views.py and load them into the DOM as a Single Page Application
// when the page loads
document.addEventListener('DOMContentLoaded', function() {
    fetch('/load_posts')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const postList = document.getElementById('post-list');
            if (!data.posts) {
                console.log('No posts found');
                return;
            }
            try {
                data.posts.forEach(post => {
                    console.log(post);
                    const postItem = document.createElement('div');
                    postItem.className = 'post-item';
                    postItem.innerHTML = `
                        <p><strong>${post.author}</strong></p>
                        <p>${post.text}</p>
                        <p>${post.timestamp}</p>
                        <p>Liked by: ${post.liked_by.join(', ')}</p>
                        <p>Comments: ${post.comments}</p>
                    `;
                    console.log(postItem);
                    postList.appendChild(postItem);
                });
            } catch (error) {
                console.error('Error:', error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        })
});

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
                postList.appendChild(postItem);
            }
            console.log("Post has been submitted!");
        });
}); 