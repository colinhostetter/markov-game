import * as React from "react";
import classnames from "classnames";
import "./TimerBar.css";

const TICK_RATE_MS = 30;

class TimerBar extends React.Component {
  constructor({ wordNum, countdownSecs }) {
    super();
    this.state = { timeLeft: countdownSecs };
  }
  componentDidMount() {
    this.intervalId = setInterval(() => {
      this.setState(({ timeLeft }) => ({ timeLeft: timeLeft - (TICK_RATE_MS / 1000) }));
    }, TICK_RATE_MS);
  }
  componentWillReceiveProps({ wordNum, countdownSecs }) {
    if (wordNum !== this.props.wordNum || countdownSecs !== this.props.countdownSecs) {
      this.setState({ timeLeft: countdownSecs || this.props.countdownSecs });
    }
  }
  componentWillUnmount() {
    clearInterval(this.intervalId);
  }
  render() {
    const coverWidth = `${(1 - Math.max(this.state.timeLeft / this.props.countdownSecs, 0)) * 100}%`;
    return (
      <div className="timer-bar-container">
        <div className="timer-bar-cover" style={{width: coverWidth}} />
        <div className={classnames("timer-bar", this.props.className)} />
      </div>
    );
  }
}

export default TimerBar;
