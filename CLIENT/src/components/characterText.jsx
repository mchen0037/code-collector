import React, { Component } from 'react';
//IMPORT IMAGE
import JIJI from "../assets/img/jiji.jpg";

//IMPORT JS
import {popOut} from "../assets/js/popOutText.js";
import {sendText} from "../assets/js/textAnimation";

class characterText extends Component {
    state = {  }
    render() { 
        return (
            <React.Fragment>
                <div className = "characterText">
                <div className = "popup" id = "textPosition">
                    <div className = "popuptext" id = "myPopup">To turn the red light on for 5 seconds, type:<br/><br/><pre>red.on()<br/>wait(5)</pre><br/>and press the Play button</div>
                </div>
                    <center><img alt = "" onClick = {()=> popOut()} onClick = {()=> sendText()} className = "characterTalks" src = {JIJI}/></center>
                </div>
            </React.Fragment>
          );
    }
}
 
export default characterText;
