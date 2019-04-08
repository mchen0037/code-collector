import React, { Component } from 'react';
import {Grid, Message, Form, Input, Label, Button} from "semantic-ui-react";

class Problem extends Component {
  constructor(props) {
    super(props)
    this.handleSecond = this.handleSecond.bind(this);
    this.handleFirst = this.handleFirst.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }
  state = {
    student_1: "",
    student_2: ""
  }

  handleFirst(e) {
    this.setState({student_1: e.target.value})
  }

  handleSecond(e) {
    this.setState({student_2: e.target.value})
  }

  handleClick() {
    this.props.setStudents(this.state.student_1, this.state.student_2)
  }

  render() {
    return (
      <Grid padded centered>
        <Grid.Row>
          <Grid.Column width={5}>
            <center>
              <h2>Login!</h2>
            </center>
              <Message>
                <Form>
                  <Form.Field>
                    <Label>Student 1</Label>
                    <Input placeholder='Student Name..'
                      value={this.state.student_1} onChange={this.handleFirst}/>
                  </Form.Field>
                  <Form.Field>
                    <Label>Student 2</Label>
                    <Input placeholder='Student Name..'
                      value={this.state.student_2} onChange={this.handleSecond}/>
                  </Form.Field>
                  <center>
                    <Button type='submit' primary onClick={this.handleClick}>
                      Submit
                    </Button>
                  </center>
                </Form>
              </Message>
          </Grid.Column>
        </Grid.Row>
      </Grid>
    )
  }
};

export default Problem;
