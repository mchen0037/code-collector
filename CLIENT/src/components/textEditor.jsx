import React, { Component } from 'react';
import AceEditor from 'react-ace';
import axios from "axios";

import 'brace/mode/python';
import 'brace/theme/xcode';

//IMPORT SEMANTIC UI
import {Button, Icon, Grid} from "semantic-ui-react";

//IMPORT JS
import {updateValue, returnCode, userInput} from "../assets/js/popOutText";

const _SERVER = "http://0.0.0.0:5000";

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
        // console.log(code.input);
        axios.post(_SERVER + "/run", {code})
        .then(res =>{
            // console.log(res.data)
            //UPDATES WHAT WILL BE DISPLAY OJN CONSOLE
            axios.get(_SERVER + "/output")
            .then(res => {
                const output = res.data;
                console.log(res.data)
                this.setState({output});
            })
        })
    }

    handleKill = () =>{
        axios.get(_SERVER + "/kill")
        .then(res => {
            console.log(res.data);
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
