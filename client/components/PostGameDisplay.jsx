import * as React from "react";
import ScoreDisplay from "./ScoreDisplay";
import constants from "../constants";
import "./PostGameDisplay.css";

class PostGameDisplay extends React.Component {
  render() {
    const score = this.props.guessesCorrect.filter(i => i === true).length;
    let commentary;
    if (score === constants.ROUNDS_PER_GAME) {
      commentary = "Wow!!!";
    } else if (score / constants.ROUNDS_PER_GAME >= 0.7) {
      commentary = "Nice job!";
    } else if (score / constants.ROUNDS_PER_GAME >= 0.4) {
      commentary = "Not bad!"
    } else {
      commentary = "Oops, better luck next time!";
    }
    return (
      <div className="post-game-display">
        <ScoreDisplay guessesCorrect={this.props.guessesCorrect} />
        <div className="padded-edges">
          <p>You and your partner scored {score} points out of {constants.ROUNDS_PER_GAME}! {commentary}</p>
          <a href="/"><button className="main-menu-button">Back to menu</button></a>
        </div>
      </div>
    )
  }
}

export default PostGameDisplay;
