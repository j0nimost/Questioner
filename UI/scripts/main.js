function input_error(){
    /*get all elements*/
    
    var elements = document.querySelectorAll("form  input[type='text']")

    for (var i = 0, element; element = elements[i++];) {
        if (element.value === ""){
            document.getElementById("err").className =' '  
        }
            
}
}


up = 0;
down = 0;

function voteupcount(){
    up = parseInt(up) + parseInt(1)
    var spanval = document.getElementById('upcount')
    spanval.innerHTML = up + ' votes'
}

function votedowncount(){
    down = parseInt(down) + parseInt(1)
    var spanval = document.getElementById('downcount')
    spanval.innerHTML = down + ' votes'
}

function enablecomment() {
    var comment = document.getElementsByClassName('comments')

    for (var i = 0; i < comment.length;i+=1){
        if (comment[i].style.display === 'none'){
            comment[i].style.display = 'block'
        } else {
            comment[i].style.display = 'none'
        }    
    }
}


function enableadmin() {
    var delete_btn = document.getElementsByName('delete')
    var create_meetup = document.getElementById('create');


        /* for create section */
        if (create_meetup.style.display === 'none') {
            create_meetup.style.display = 'block';
        } else {

            create_meetup.style.display = 'none'
        }

        /*for delete buttons */
        for (var i = 0; i < delete_btn.length; i += 1){
            if (delete_btn[i].style.display === 'none') {
                delete_btn[i].style.display = 'block'
            } else {
                delete_btn[i].style.display = 'none'
            }
        }
    return false;
}