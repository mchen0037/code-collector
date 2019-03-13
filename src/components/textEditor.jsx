import React, { Component } from 'react';
import AceEditor from 'react-ace';
import axios from "axios";

import 'brace/mode/python';
import 'brace/theme/xcode';

//IMPORT SEMANTIC UI
import {Button, Icon} from "semantic-ui-react";

//IMPORT JS
import {updateValue, returnCode} from "../assets/js/popOutText";

class textEditor extends Component {
    state = {
        // code: ""
    }
    
    handleChange = (code) =>{
        updateValue(code);
    }
    //will handle submission of code written
    handleRun = () =>{
        const code = {
            code1: returnCode()
        }
        axios.post("", {code})
        .then(res =>{
            console.log("cool post");
        })
    }
    render() { 
        return (
            <React.Fragment>
                  <AceEditor
                    className = "editor"
                    fontSize = {18}
                    mode="python"
                    theme="xcode"
                    onChange={this.handleChange}
                    name="UNIQUE_ID_OF_DIV"
                    editorProps={{$blockScrolling: true}}
                  />
                  <div className = "buttonRun">
                    <Button animated className = "runPlay" onClick = {() => this.handleRun()}>
                        <Button.Content visible>
                            <Icon name='pause' />
                        </Button.Content>
                        <Button.Content hidden>
                            <Icon name='play' />
                        </Button.Content>
                    </Button>
                  </div>
               
                  <textarea className = "console" type ="text" name = "comment" 
                 placeholder="The original Super Smash Bros., released in 1999 for the Nintendo 64, had a small budget and was originally a Japan-only release, but its domestic success led to a worldwide release. The series achieved even greater success with the release of Super Smash Bros. Melee, which was released in 2001 for the GameCube and became the bestselling game on that system. A third installment, Super Smash Bros. Brawl, was released in 2008 for the Wii. Although HAL Laboratory had been the developer of the first two games, the third game was developed through the collaboration of several companies. The fourth installment, Super Smash Bros. for Nintendo 3DS and Wii U, were released in 2014 for the Nintendo 3DS and Wii U, respectively. The 3DS installment was the first for a handheld platform. A fifth installment, Super Smash Bros. 
                  Ultimate, was released in 2018 for the Nintendo Switch."/>
                 
            </React.Fragment>
          );
    }
}
 
export default textEditor;