var words = `<bubble>
<message>
Let's turn on the red light for 1 second. We can refer to each of the lights by name (red, yellow, green), and we can instruct each of them to turn on or off. We do this by adding the command to the name, like this:

<code>red.on()</code>

After this, we need to tell the computer to wait for a certain period of time, so that the light stays on for that period. To do this, just type:

<code>wait(5)</code>

Now, turn on the red light for 5 seconds.
</message>
<output>
AA: red turning on
AA: waiting 5 seconds
</output>
</bubble>

<bubble>
<message>
Now it is the next thing...
</message>
<output>
AA: Whatever
</output>
</bubble>`

//HERE WILL BE FUNCTION THAT WILL PARSE STRING IN THER CORRESPONDING SECTIONS
//READ MESSAGE FROM READ FILE TEXT

// GET BUBBLE ELEMENTS
var startScript = 0;
var storeBubbles = [];
let endBubble;
let newBubbleSlice = "";
let completeScript = 0
while((completeScript) < words.length){
    newBubbleSlice = words.slice(startScript);
    startScript = newBubbleSlice.search("<bubble>");
    endBubble = newBubbleSlice.search("</bubble>");
    storeBubbles.push(newBubbleSlice.substring((startScript + 8), (endBubble - 1)));
    startScript = endBubble + 9;
    completeScript += startScript;
    console.log(startScript);
}
    // newBubbleSlice = words.slice(startScript);
    // console.log("NEW BUBBLE: ", newBubbleSlice);
console.log("BUBBLE ARRAY: ", storeBubbles);

console.log(message);

var bubbleIndex = 0; //used to move between bubbles
var indexWord = 0; // used to keep track of message and code element for each bubble
var textAnimation;
var textFinished = false;
//CODE TAG HELPERS
var startCode = false;
var createLineCode = true;
var endCode;
var newCode;
var actualCode = "";
var text = document.getElementsByClassName("popuptext");

//function used to repeat content again
export function repeatAgain(res){
    if(res === "YES"){
        indexWord = 0;
        textFinished = false;
        text[0].style.height = "none";
        text[0].innerHTML = "";
        document.getElementById("repeatContent").style.display = "none";
    }
    else if(res === "NO"){
        text[0].innerHTML = "OKAY, GOOD LUCK!!!";
        document.getElementById("repeatContent").style.display = "none";
        if((bubbleIndex + 1) < storeBubbles.length)
            bubbleIndex += 1;
        textFinished = false; //TEMPORARY DEMO PURPOSE
        startBubble = true;
        text[0].innerHTML = "";
        console.log(message);
    }
}

//HANDLE WHEN NEXT BUBBLE WILL BE FETCHED
var startBubble = true;
var message = "";
var output = "";
function startNewBubble(){
    let startIndex = storeBubbles[bubbleIndex].search("<message>") + 10;
    let endIndex = storeBubbles[bubbleIndex].search("</message>");
    while(startIndex < endIndex){
        message += storeBubbles[bubbleIndex][startIndex];
        startIndex +=1;
    }
    //OUTPUT HEEEERE
    let startOutput = storeBubbles[bubbleIndex].search("<output>");
    let endOutput = storeBubbles[bubbleIndex].search("</output>") - 8;
    console.log(endOutput);
    output = (storeBubbles[bubbleIndex].substr(startOutput + 8, (endOutput)));
}

//called everytime we click on cat
export function sendText(){
    if(startBubble){
        startNewBubble();
        startBubble = false;
    }
    if(!textFinished === true){
        console.log("FETCHED??? ",message)
        text[0].style.height = "none";
        text[0].innerHTML = "";
        textAnimation = setInterval(display, 5);
    }
}

//display words in animation format
function display(){
    if(indexWord < message.length){
        let temp = indexWord;
        if((message[indexWord] === '<' && message[indexWord + 1] === 'c' 
        && message[indexWord + 2] === 'o') || startCode){
            startCode = true;
            if(createLineCode){
                text[0].innerHTML += "<br/>";
                createLineCode = false;
                //cut message to get next coding tag
                newCode = message.slice(indexWord);
                endCode = newCode.search("</code>") + indexWord;
                indexWord += 5;
            }
            else{
                let ready = false;
                if(indexWord === (endCode - 1)){
                    console.log(indexWord, " > ", endCode);
                    indexWord += 8;
                    text[0].innerHTML += "<br/>";
                    createLineCode  = true;
                    startCode = false;
                    ready = true;
                }
                if(ready){
                    text[0].innerHTML += "<pre class = 'codeWritten'>" + actualCode + "</pre>";
                    text[0].innerHTML += "<br/>";
                    actualCode = "";
                }
                else{
                    indexWord +=1;
                    actualCode += message[indexWord];
                }
            }
        }
        else{
            startCode = false;
            text[0].innerHTML += message[indexWord];
            indexWord +=1;
            console.log(text[0].offsetHeight);
        }
        if(text[0].offsetHeight > 200 && message[temp] === ' '){
            clearInterval(textAnimation);
        }
        if(indexWord === message.length){
            textFinished = true;
            document.getElementById("repeatContent").style.display = "block";
        }
    }
}


