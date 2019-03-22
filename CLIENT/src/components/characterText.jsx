import React, { Component } from 'react';
//IMPORT IMAGE
import JIJI from "../assets/img/jiji.jpg";

import {Button} from "semantic-ui-react";

//IMPORT JS
import {sendText, repeatAgain} from "../assets/js/textAnimation";

class characterText extends Component {
    state = {  }
    render() { 
        return (
            <React.Fragment>
                <div className = "characterText">
                <div className = "popup" id = "textPosition">
                    <div className = "popuptext" id = "myPopup">HELLO THERE!!!</div><br/>
                </div>
                    <center><img alt = "" onClick = {()=> {sendText()}} className = "characterTalks" src = {JIJI}/></center>
                    <div id = "repeatContent">
                        <center>
                            <br/>
                            <h1>Would You Like Me To Repeat That Again?</h1>
                            <div>
                                <Button onClick = {()=>repeatAgain("YES")} content='YES' primary />
                                <Button onClick = {()=>repeatAgain("NO")} content='NO' secondary />
                            </div>
                        </center>
                    </div>
                </div>
            </React.Fragment>
          );
    }
}
 
export default characterText;