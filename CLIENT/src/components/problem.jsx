import React, { Component } from 'react';
import {Container, Header} from "semantic-ui-react";
import Plot from 'react-plotly.js';

class Problem extends Component {
  render() {
    return (
        <Container className="problem" text>
          <Header as='h2'>RC Cola Contest!</Header>
          <p>
            RC Cola is having a promotional contest in order to make a
            comeback in the soda industry! They label numbers on the bottom
            of each soda cap from <b>1-6</b>.<b>If you happen
            to get a bottle with the number '1' on it, you win the prize</b>!
          </p>
          <p>
            This is a prize you NEED: Guaranteed admission to your dream
            college, all the skins in Fortnite, your chance to meet any
            celebrity.. You've completely lost your mind and
            <b> you won't stop buying sodas until you've bought a soda with a
            '1' on the cap</b>. You go up to an infinite RC Cola machine and do
            just that.
          </p>
          <p>
            Now suppose 10,000 people line up behind you because they also
            want this prize. Every one is waiting in this line so that they
            can do the exact same thing: Buy a soda, check the number.. 3? Buy a
            soda, check the cap to see if it's a 1-- 6? Buy a soda, check the
            cap to see if it's a 1--yes! Out of excitement, people scream
            <b>how many bottles they bought in total</b>.
          </p>
          <p>
            Researcher Helen Zhao Chen is curious to see which number was
            most likely to be shouted. She stands next to the RC Cola
            machine with a clipboard and <b>makes a list</b> of the numbers that
            people are shouting. Every time somebody shouts a number, she
            <b> appends it to her list</b>.
          </p>
          <p>
            Print out this list that Helen has on her clipboard.
          </p>
          <center>
            <Plot className="plot"
              data={[
                {
                  x: this.props.data,
                  type: 'histogram',
                }
              ]}
              layout={{
                width: 600,
                height: 375,
                title: "How many Tries until Prize?",
                xaxis: {title: "Number of Tries"},
                yaxis: {title: "Number of People"}
              }}
            />
          </center>
        </Container>
    )
  }
};

export default Problem;
