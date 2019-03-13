export function popOut(){
    var popup = document.getElementsByClassName("popuptext");
    if(popup[0].style.display === "block"){
        popup[0].style.display = "none";
    }
    else{
        popup[0].style.display = "block";
    }
}

var code1 = "";
export function updateValue(code){
    code1 = code;
    console.log(code1);
}

export function returnCode(){
    return code1;
}