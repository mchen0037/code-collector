import React, { Component } from 'react';

//IMPORT COMPONENTS
import TextEditor from "./components/textEditor";
import CharacterText from "./components/characterText";

//IMPORT SEMANTIC UI
import {Grid} from "semantic-ui-react";

//IMPORT CSS
import "./assets/css/textEditor.css";

class App extends Component {
  render() {
    return (
     <React.Fragment>
       <Grid columns= "equal">
        <Grid.Column width = {8}>
          <TextEditor/>
        </Grid.Column>
        <Grid.Column width = {8}>
          <CharacterText/>
        </Grid.Column>
      </Grid>
     </React.Fragment>
    );
  }
}

export default App;