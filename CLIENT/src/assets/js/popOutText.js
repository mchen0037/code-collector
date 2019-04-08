import axios from "axios";
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
    // console.log(code1);
}

export function returnCode(){
    return code1;
}

//USED TO PARSE USER INPUT
export function userInput(code) {
    var found = (code.match(/raw_input()/g) || []).length
    var total = ''
    var i = 1
    if (found === 0) {
      return total
    }
    else {
      var test = (code.match(/raw_input()/) || []).input.split(/['']/)
      while (found !== 0) {
        var userInput = prompt(test[i])
        total += userInput + '\n'
        i = i + 2
        found--
      }
    }
    return total
  }

const _SERVER = "http://0.0.0.0:5000";
// const _SERVER = "https://rc-cola-backend.herokuapp.com"
export async function uploadCode(group_id) {
  group_id = group_id
  while (true) {
    // console.log(code1)
    // wait 10 seconds
    axios.post(_SERVER + "/upload", {code1, group_id})
    await new Promise((resolve, reject) => setTimeout(resolve, 10000));

  }
}
