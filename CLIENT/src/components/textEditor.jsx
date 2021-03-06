import React, { Component } from 'react';
import AceEditor from 'react-ace';
import axios from "axios";

import 'brace/mode/python';
import 'brace/theme/xcode';

//IMPORT SEMANTIC UI
import {Button, Icon, Grid} from "semantic-ui-react";

//IMPORT JS
import {updateValue, returnCode, userInput, uploadCode} from "../assets/js/popOutText";

// const _SERVER = "http://0.0.0.0:5000";
const _SERVER = "https://rc-cola-backend.herokuapp.com"

// https://stackoverflow.com/questions/4456336/finding-variable-type-in-javascript
var isArray = function (obj) {
  switch (typeof(obj)) {
    case 'object':
      if (obj instanceof Array)
        return true;
      if (obj instanceof String)
        return false;
      return false;
    default:
      return false;
  }
};

class textEditor extends Component {
  constructor(props) {
    super(props)
    uploadCode(this.props.group)
    console.log(this.props.init)
    updateValue(this.props.init)
  }

  state = {
    output: "",
    running: false,
    ticket: ""
  }

  handleChange = (code) =>{
    updateValue(code);
  }
  //will handle submission of code written
  handleRun = () => {
    this.setState({running: true})
    const code = {
        code: returnCode(),
        input: userInput(returnCode()),
        group: this.props.group
    }
    // console.log(code.input);
    axios.post(_SERVER + "/run", {code})
    .then(res =>{
        this.setState({output: res.data, running: false})
        if (isArray(res.data)) {
          this.props.setData(res.data)
        }
        // this.setState({ticket: res.data})
        // UPDATES WHAT WILL BE DISPLAY ON CONSOLE
        // axios.get(_SERVER + "/output", {
        //   params: {
        //     ticket: this.state.ticket
        //   }
        // })
        // .then(res => {
        //     const output = res.data;
        //     // console.log(res.data)
        //     if (isArray(res.data)) {
        //       this.props.setData(res.data)
        //     }
        //     this.setState({output: output, running: false});
        // })
      })
  }

  handleKill = () =>{
      axios.get(_SERVER + "/kill", {
        params: {
          ticket: this.state.ticket
        }
      })
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
                {!this.state.running ?
                  <Button id = "playButton" className = "runPlay" onClick = {() => this.handleRun()}>
                    <Button.Content hidden>
                        <Icon name='play' />
                    </Button.Content>
                  </Button>
                  :
                  <Button id="playButton" className="runPlay" loading>
                    <Button.Content hidden>
                      <Icon name='play'/>
                    </Button.Content>
                  </Button>
                }
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
          <div className="console" type="text" name="comment">
            {isArray(this.state.output) ?
              <pre>{JSON.stringify(this.state.output)}</pre> :
              <pre>{this.state.output}</pre>
            }
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default textEditor;
