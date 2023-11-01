document.addEventListener('DOMContentLoaded', function() { 
    let currentPage = 1;	
    const postsPerPage = 10;
    let loadMorePosts = false;
    let allPostsLoaded = false;
    
    // Function to fetch and display all posts from server
    function fetchAndDisplayPosts(page) {
        if (loadMorePosts || allPostsLoaded) {
            return;
        }

        loadMorePosts = true;
        const loadingText = document.getElementById('loading-text');
        loadingText.textContent = 'Loading...';

        fetch(`/get_posts?page=${page}`)
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

                currentPage++;
                loadMorePosts = false;

                if (data.posts.length < postsPerPage) {
                    allPostsLoaded = true;
                    loadingText.textContent = 'All posts loaded';
                } else {
                    loadingText.textContent = 'Loading...';
                }
            })        
            .catch(error => {
                console.error('Error fetching and displaying posts:', error);
                loadMorePosts = false;
                loadingText.textContent = '';
            });
    }   
    
    let timeout;
    window.addEventListener('scroll', function() {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
            this.clearTimeout(timeout);
            timeout = setTimeout(() => {
                fetchAndDisplayPosts(currentPage);
            }, 1000);
        }
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
                    postList.insertBefore(postItem, postList.firstChild);
                }
                console.log("Post has been submitted");
                const textarea = document.getElementById('post-content');
                textarea.value = '';
            });
    }); 

    fetchAndDisplayPosts(currentPage);
});