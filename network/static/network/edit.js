document.addEventListener('DOMContentLoaded', function() {
    let like_buttons = document.querySelectorAll('span');
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
    let btns = document.querySelectorAll('small');
        for (i of btns) {
            i.addEventListener('click', function(event) {
            let id = event.srcElement.id;
            console.log(id.slice(id.length - 2));            
            document.querySelector(`#${event.srcElement.id}-content`).style.display = 'none';
            document.querySelector(`#${event.srcElement.id}_content`).style.display = 'block';
            document.querySelector(`#${event.srcElement.id}-form`).addEventListener('submit', () => {
                document.querySelector(`#${event.srcElement.id}_content`).style.display = 'none';
                let new_text = document.querySelector(`#${event.srcElement.id}-text`).value;
                let id = event.srcElement.id;
                let ib = id.slice(id.length - 2);
                console.log(id.slice(id.length - 2));
                event.preventDefault();
                fetch(`/edit/${ib}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        content: new_text,
                    })
                })
                .then((event) => {
                    console.log(event)
                    event.preventDefault();
                    return false;
                });
            event.preventDefault();   
            });
            
        });    
    }    
});



