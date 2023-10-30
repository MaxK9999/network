// Imply logic to post, load and edit submitted posts
document.addEventListener('DOMContentLoaded', function() {

    console.log('Hello there!')


    // Post-list container
    const postList = document.getElementById('post-list');

    // Load and display posts
    function loadPosts() {
        fetch('/load_posts')
            .then(response => response.json())
            .then(data => {
                postList.innerHTML = '';
                console.log(data)

                data.posts.posts.forEach(post => {
                    const postItem = document.createElement('div');
                    postItem.className = 'post-item';

                    // Post structure
                    postItem.innerHTML = `
                        <p><strong>${post.user}</strong></p>
                        <p>${post.body}</p>
                        <p>${post.timestamp}</p>
                        <p>Liked by: ${post.liked_by.join(', ')}</p>
                        <p>Comments: ${post.comments}</p>
                    `;

                    postList.appendChild(postItem);
                });
            });
    }
    loadPosts();

    // Form submission
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
            if (data.message === 'Post created succesfully!') {
                loadPosts();
            }
        });
    });
});