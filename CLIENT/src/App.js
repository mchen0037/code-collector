import React, { Component } from 'react';

//IMPORT COMPONENTS
import TextEditor from "./components/textEditor";
import Problem from "./components/problem.jsx";
import Login from "./components/login.jsx";

//IMPORT SEMANTIC UI
import {Grid} from "semantic-ui-react";
import axios from "axios";

//IMPORT CSS
import "./assets/css/textEditor.css";

const _SERVER = "http://0.0.0.0:5000";
// const _SERVER = "https://rc-cola-backend.herokuapp.com"

class App extends Component {
  constructor() {
    super()
    this.handleGetData = this.handleGetData.bind(this);
    this.handleLogin = this.handleLogin.bind(this);
  }

  state = {
    data: [],
    student_1: "",
    student_2: ""
  }

  handleGetData = (arr) => {
    this.setState({data: arr})
  }

  handleLogin(st_1, st_2) {
    this.setState({student_1: st_1, student_2: st_2})
    axios.post(_SERVER + "/login", {st_1, st_2})
  }

  render() {
    return (
      <div>
        {this.state.student_1 ?
          <React.Fragment>
            <Grid columns= "equal" padded>
              <Grid.Column width = {8}>
                <TextEditor setData={this.handleGetData}/>
              </Grid.Column>
              <Grid.Column width = {8}>
                <Problem data={this.state.data}/>
              </Grid.Column>
            </Grid>
          </React.Fragment>
          :
          <Login setStudents={this.handleLogin}/>
        }
      </div>
    );
  }
}

export default App;