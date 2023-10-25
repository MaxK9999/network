function create_post() {
    // Create a new post
    const postContent = document.querySelector('#post-content').value;
  
    // Create a JSON object with the 'content' field
    const data = {
      content: postContent
    };
  
    fetch('/new_post', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') // Include CSRF token
      },
      body: JSON.stringify(data),
    });
  }
  
  // Function to get CSRF token from cookies
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
  