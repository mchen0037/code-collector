import React, { Component } from 'react';

//IMPORT COMPONENTS
import TextEditor from "./components/textEditor";

//IMPORT SEMANTIC UI
import {Grid, Container, Header} from "semantic-ui-react";

//IMPORT CSS
import "./assets/css/textEditor.css";

class App extends Component {
  render() {
    return (
     <React.Fragment>
       <Grid columns= "equal" padded>
        <Grid.Column width = {8}>
          <TextEditor/>
        </Grid.Column>
        <Grid.Column width = {8}>
          {/* <CharacterText/> add a block of text here describing the
            RC cola problem isntead.*/}
            <Container text>
              <Header as='h2'>RC Cola Contest!</Header>
              <p>
                RC Cola is having a promotional contest in order to make a
                comeback in the soda industry! They label numbers on the bottom
                of each soda cap from 1-6, so that you have an equal chance of
                getting a bottle with any number on it. If you happen to get a
                bottle with the number '1' on it, you win the prize!
              </p>
              <p>
                This is a prize you NEED: Guaranteed admission to your dream
                college, all the skins in Fortnite, your chance to meet any
                celebrity.. you name it! You've completely lost your mind and
                you won't stop buying sodas until you've bought a soda with a
                '1' on the cap. You go up to an infinite RC Cola machine and do
                just that: you buy sodas until you open one with your prize.
              </p>
              <p>
                Now suppose 10,000 people line up behind me because they also
                want this prize. Everyone is awiting in this line so that they
                can do the exact same thing: Buy a soda, check the cap to see if
                it's a 1--no? Buy a soda, check the cap to see if it's a 1-- no?
                Buy a soda, check the cap to see if it's a 1--yes! Let's say
                everyone got so excited, they shouted out the number of bottles
                they had to buy to get their win, before leaving to go home.
              </p>
              <p>
                Researcher Helen Zhao Chen is curious to see which number was
                most likely to be shouted. She stands next to the RC Cola
                machine with a clipboard and makes a list of the numbers that
                people are shouting. Every time somebody shouts a number, she
                appends it to her list.
              </p>
              <p>
                Define a function called cola( ) which returns this list. You
                will see a histogram (how many times each number was shouted
                out) below.
              </p>
            </Container>
        </Grid.Column>
      </Grid>
     </React.Fragment>
    );
  }
}

export default App;
