var index = 0;
var indexWord = 0;
var textAnimation;
var words = "Like opossums, mice, and moles, hedgehogs have some natural immunity against some snake venom through the protein erinacin in the animal's muscular system, although it is available only in small amounts and a viper bite may still be fatal.[7] In addition, hedgehogs are one of four known mammalian groups with mutations that protect against another snake venom, α-neurotoxin. Pigs, honey badgers, mongooses, and hedgehogs all have mutations in the nicotinic acetylcholine receptor that prevent the snake venom α-neurotoxin from binding, though those mutations developed separately and independently.[8]";
var text = document.getElementsByClassName("popuptext");
export function sendText(){
    console.log("COOL");
    textAnimation = setInterval(display, 5);
}


function display(){
    if(indexWord < words.length){
        text[0].innerHTML += words[indexWord];
        indexWord +=1;
    }
    else{
        clearInterval(textAnimation);
    }
}


