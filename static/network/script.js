document.addEventListener("DOMContentLoaded", () => {
    const postContentInput = document.getElementById("postContent");
    const postImageInput = document.getElementById("postImage");
    const submitButton = document.getElementById("submitPost");
    const postList = document.getElementById("postList");
    const posts = []; // Store posts in memory

    // Function to render posts
    function renderPosts() {
        postList.innerHTML = "";
        posts.forEach((post) => {
            const postDiv = document.createElement("div");
            postDiv.innerHTML = `
                <h3>${post.user}</h3>
                <p>${post.body}</p>
                ${post.image ? `<img src="${URL.createObjectURL(post.image)}" alt="Post">` : ""}
                <p>Posted on ${post.timestamp.toISOString()}</p>
            `;
            postList.appendChild(postDiv);
        });
    }

    // Function to handle post submission
    function submitPost() {
      const content = postContentInput.value;
      const image = postImageInput.files[0];
      
      // Create a new post object
      const newPost = {
          user: "Current User",
          body: content,
          image: image,
          timestamp: new Date(),
          likes: [],
      };

      // Send the new post data to the server
      fetch('/new_post', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(newPost),
      })
      .then(response => response.json())
      .then(data => {
          console.log(data.message);
      })
      .catch(error => {
          console.error('Error:', error);
      });

      // Clear input fields
      postContentInput.value = "";
      postImageInput.value = "";
    }

});
