document.addEventListener('DOMContentLoaded', function() {
    console.log('loaded');
    let btns = document.querySelectorAll('small');
        for (i of btns) {
            i.addEventListener('click', function(event) {
            console.log(this);
            console.log(event.srcElement.id);
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
                console.log(new_text)
                fetch(`/edit/${ib}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        content: new_text,
                    })
                })
                .then(() => {
                    preventDefault();
                    return false;
                });
               
            });
        return false;    
        });
    
    }    
});



