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
