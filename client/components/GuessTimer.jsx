import * as React from "react";
import TimerBar from "./TimerBar";
import constants from "../constants";
import "./GuessTimer.css";

class GuessTimer extends React.Component {
  constructor(props) {
    super(props);
    this.state = { secondsLeft: constants.GUESS_TIME_SECONDS };
  }
  componentDidMount() {
    this.intervalId = setInterval(() => {
      this.setState(({ secondsLeft }) => ({ secondsLeft: Math.max(secondsLeft - 1, 0) }));
    }, 1000);
  }
  componentWillUnmount() {
    clearInterval(this.intervalId);
  }
  render() {
    const guesserHas = this.props.guessing ? "You have" : "Your partner has"
    return <div>
      <TimerBar countdownSecs={constants.GUESS_TIME_SECONDS} className="guess-timer-bar" />
      <div className="guess-timer">{guesserHas} {this.state.secondsLeft} seconds left to guess!</div>
    </div>
  }
}

export default GuessTimer;
