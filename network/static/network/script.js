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
                        <p class="post-author"><strong><a href="/profile_page/${post.author}">${post.author}</a></strong></p>
                        <button class="edit-button">Edit</button>
                        <button class="save-button" style="display: none;">Save</button>
                        <button class="delete-button">Delete</button>
                        <div class="post-text">
                            <p data-post-id="${post.id}">${post.text}</p>
                        </div>
                        <p>${post.timestamp}</p>
                        <div class="likes-comments">
                            <p>Liked by: ${post.liked_by.join(', ')}</p>
                            <p>Comments: ${post.comments.length}</p>
                        </div>
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

    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    function handleEditPost(postItem) {
        const editButton = postItem.querySelector('.edit-button');
        const saveButton = postItem.querySelector('.save-button');
        const postContent = postItem.querySelector('.post-text');
        const originalText = postContent.textContent;

        if (editButton.textContent === 'Edit') {
            editButton.textContent = 'Cancel';
            saveButton.style.display = 'inline';
            postContent.contentEditable = true;
            postContent.focus();
        } else {
            editButton.textContent = 'Edit';
            saveButton.style.display = 'none';
            postContent.contentEditable = false;
            postContent.textContent = originalText;
        }
    }

    function handleSavePost(postItem) {
        const postContent = postItem.querySelector('.post-text');
        const postId = postContent.querySelector('p').dataset.postId;
        const editedText = postContent.querySelector('p').textContent;

        fetch(`/edit_post/${postId}`, {
            method: 'POST',
            body: JSON.stringify({ text: editedText }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),	
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'Post edited successfully!') {
                postContent.querySelector('p').textContent = editedText;
                handleEditPost(postItem);
            }
        })
        .catch(error => {
            console.error('Error editing post:', error);
        });
    }

    document.addEventListener('click', function(event) {
        const target = event.target;
        if (target.classList.contains('edit-button')) {
            const postItem = target.closest('.post-item');
            handleEditPost(postItem);
        } else if (target.classList.contains('save-button')) {
            const postItem = target.closest('.post-item');
            handleSavePost(postItem);
        }
    });

    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + '=') {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

   
    let timeout;
    window.addEventListener('scroll', function() {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
            this.clearTimeout(timeout);
            timeout = setTimeout(() => {
                fetchAndDisplayPosts(currentPage);
            }, 1000);
        }
    });
     
    fetchAndDisplayPosts(currentPage);
    	

    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // Form submission
    const postForm = document.getElementById('post-form');
    postForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(postForm);
        const textarea = formData.get('body');
        const formattedText = textarea.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\n/g, '<br>');
        formData.set('body', formattedText);

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
                        <p class="post-author"><strong>${data.post.user}</strong></p>
                        <p>${data.post.body}</p>
                        <p>${data.post.timestamp}</p>
                        <div class="likes-comments">        
                            <p>Liked by: ${data.post.liked_by.join(', ')}</p>
                            <p>Comments: ${data.post.comments}</p>
                        </div>
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