document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.post-edit').forEach(editLink => {
        editLink.addEventListener('click', function (event) {
            event.preventDefault();

            const post_id = parseInt(editLink.id.split('-')[1]);

            editPost(post_id);
        });
    });

    document.querySelectorAll('.post-likes').forEach(postLikes => {
        postLikes.addEventListener('click', function (event) {
            event.preventDefault();

            const post_id = parseInt(postLikes.id.split('-')[1]);

            like(post_id);
        });
    });


    function editPost(post_id) {
        const postContentDiv = document.getElementById(`content-${post_id}`);
        const postContent = postContentDiv.innerText;

        postContentDiv.innerHTML = `
            <textarea id="textarea-${post_id}" class="edit-textarea">${postContent}</textarea>
            <button class="btn btn-primary btn-sm save-btn">Save</button>
            <button class="btn btn-secondary btn-sm cancel-btn">Cancel</button>
        `;

        postContentDiv.querySelector('.save-btn').addEventListener('click', function () {
            savePost(post_id);
        });
        postContentDiv.querySelector('.cancel-btn').addEventListener('click', function () {
            cancelEdit(post_id, postContent);
        });
    }


    function savePost(post_id) {
        const textarea = document.getElementById(`textarea-${post_id}`);
        const newContent = textarea.value;

        fetch(`/edit/${post_id}/`, {
            method: 'PUT',
            body: JSON.stringify({
                content: newContent
            })
        })
        .then(response => {
            if (response.ok) {
                const postContentDiv = document.getElementById(`content-${post_id}`);
                postContentDiv.innerText = newContent;
            } else {
                return response.json().then(data => {
                    console.error(data.error);
                });
            }
        })
        .catch(error => {
            console.error('Error saving post:', error);
        });
    }


    function cancelEdit(post_id, post_content) {
        const postContentDiv = document.getElementById(`content-${post_id}`);
        postContentDiv.innerText = post_content;
    }


    function like(post_id) {
        fetch(`/like/${post_id}/`, { method: 'POST' })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to like post');
                }
                return response.json();
            })
            .then(data => {
                const likeCountElement = document.getElementById(`like-count-${post_id}`);
                likeCountElement.innerText = data.likes_count;
    
                const likeIcon = data.is_liked ? "heart.png" : "heart1.png";
                const likeImg = document.querySelector(`#likes-${post_id} img`);
                likeImg.src = `/static/network/${likeIcon}`;
            })
            .catch(error => console.error('Error:', error));
    }

});
