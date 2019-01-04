function input_error(){
    /*get all elements*/
    
    var elements = document.querySelectorAll("form  input[type='text']")

    for (var i = 0, element; element = elements[i++];) {
        if (element.value === ""){
            document.getElementById("err").className =' '  
        }
            
}
}
