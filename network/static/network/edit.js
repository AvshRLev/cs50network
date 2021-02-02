document.addEventListener('DOMContentLoaded', function() {
    
    let btns = document.querySelectorAll('small');
        for (i of btns) {
            i.addEventListener('click', function(event) {            
            document.querySelector(`#${event.srcElement.id}-content`).style.display = 'none';
            document.querySelector(`#${event.srcElement.id}_content`).style.display = 'block';
            document.querySelector(`#${event.srcElement.id}-form`).addEventListener('submit', (a) => {
                a.preventDefault();
                document.querySelector(`#${event.srcElement.id}_content`).style.display = 'none';
                let new_text = document.querySelector(`#${event.srcElement.id}-text`).value;
                let id = event.srcElement.id;
                let ib = id.slice(id.length - 2);                               
                fetch(`/edit/${ib}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        content: new_text,
                    })
                })
                .then(response => response.json())
                .then(post => {
                    if (post.status === 204) {
                        document.querySelector(`#${event.srcElement.id}_content`).style.display = 'none';
                        document.querySelector(`#${event.srcElement.id}-content`).innerHTML = post.content;
                        document.querySelector(`#${event.srcElement.id}-content`).style.display = 'block';
                    } else {
                        message = 'It has not been possible to register your edit, please try again later'
                        document.querySelector(`#${event.srcElement.id}_content`).style.display = 'none';
                        document.querySelector(`#${event.srcElement.id}-content`).style.display = 'block';
                        original_text = document.querySelector(`#${event.srcElement.id}-content`).innerHTML;
                        document.querySelector(`#${event.srcElement.id}-content`).innerHTML = message;
                        setTimeout(() => { 
                            document.querySelector(`#${event.srcElement.id}-content`).innerHTML = original_text;
                         }, 3000);
                    }
                    
                    return false;
                })    
                  
            });
            
        });    
    }
    let like_buttons = document.querySelectorAll('u');
        for (i of like_buttons) {
            i.addEventListener('click', function(event) {                
                event.preventDefault();
                let id_long = event.srcElement.id;
                id = id_long.slice(id_long.length - 2);
                fetch(`/like/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        like: 'like',
                    })
                })
                .then(response => response.json())
                .then(post => {
                    document.querySelector(`#likes${id}`).innerHTML = post.likes;
                });
                
            });
        };    
});



