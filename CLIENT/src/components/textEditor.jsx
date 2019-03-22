import React, { Component } from 'react';
import AceEditor from 'react-ace';
import axios from "axios";

import 'brace/mode/python';
import 'brace/theme/xcode';

//IMPORT SEMANTIC UI
import {Button, Icon, Grid} from "semantic-ui-react";

//IMPORT JS
import {updateValue, returnCode, userInput} from "../assets/js/popOutText";

class textEditor extends Component {
    state = {
        output: ""
    }
    
    handleChange = (code) =>{
        updateValue(code);
    }
    //will handle submission of code written
    handleRun = () =>{
        const code = {
            code: returnCode(),
            input: userInput(returnCode())

        }
        console.log("HERE ",code.input);
        axios.post("http://10.0.1.9:5000/run", {code})
        .then(res =>{
            console.log(res.data)
            //UPDATES WHAT WILL BE DISPLAY OJN CONSOLE
            axios.get("http://10.0.1.9:5000/output")
            .then(res => {
                const output = res.data;
                console.log("OUTPUT: ", res.data)
                this.setState({output});
            })
        })
    }

    handleKill = () =>{
        axios.get("http://10.0.1.9:5000/kill")
        .then(res=>{
            console.log("KILLED PROGRAM");
        })
    }
    render() { 
        return (
            <React.Fragment>
                <div className = "leftSide">
                    <AceEditor
                        className = "editor"
                        fontSize = {18}
                        value = {returnCode()}
                        mode="python"
                        theme="xcode"
                        onChange={this.handleChange}
                        name="UNIQUE_ID_OF_DIV"
                        editorProps={{$blockScrolling: true}}
                    />
                    <div className = "buttonRun">
                        <Grid columns= "equal">
                            <Grid.Column width = {8}>
                                <Button id = "playButton" className = "runPlay" onClick = {() => this.handleRun()}>
                                    <Button.Content hidden>
                                        <Icon name='play' />
                                    </Button.Content>
                                </Button>
                            </Grid.Column>
                            <Grid.Column width = {8}>
                                <Button id = "playButton" className = "runPause" onClick = {() => this.handleKill()}>
                                    <Button.Content hidden>
                                        <Icon name='pause' />
                                    </Button.Content>
                                </Button>
                            </Grid.Column>
                        </Grid>
                    </div>
                
                    <div className = "console" type ="text" name = "comment" 
                    placeholder={this.state.output}/>
                </div>
            </React.Fragment>
          );
    }
}
 
export default textEditor;
