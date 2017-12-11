import * as React from "react";
import TimerBar from "./TimerBar";
import "./SentenceDisplay.css";
import classnames from "classnames";
import constants from "../constants";

class SentenceDisplay extends React.Component {
  constructor(...args) {
    super(...args);
    this.buttons = [];
  }
  onWordButtonClicked(index) {
    this.buttons[index].blur();
    this.props.onWordChosen(index);
  }
  render() {
    const author = this.props.isPlayer ? (this.props.writing ? "You" : "Your Partner") : "Computer";
    const wordChoiceTime = this.props.wordNum === 0 ? constants.FIRST_WORD_CHOICE_TIME_SECONDS : constants.WORD_CHOICE_TIME_SECONDS
    const playerGuessingNow = this.props.status === constants.GAME_STATUS_GUESS_TIME && this.props.guessing;
    return (
      <div 
        className={classnames("sentence", playerGuessingNow && "sentence-guessing-time")}
        onClick={() => this.props.guessing && this.props.onGuessMade()}
      >
        {this.props.isGuessed &&
          <div className="guess-indicator-container">
            <div className="guess-indicator-triangle" />
            <div className="guess-indicator-box">
              <div className="guess-indicator-caption">Guess</div>
            </div>
          </div>
        }
        {(this.props.writing || this.props.status === constants.GAME_STATUS_REVEAL) &&
          <div className={classnames("author-indicator", this.props.isPlayer ? "player" : "computer")}>
            {author}
          </div>
        }
        <div className="sentence-text">
          {this.props.words.map((word, index) => <span className="word" key={index}>{word} </span>)}
        </div>
        {this.props.writing && this.props.isPlayer && this.props.status === constants.GAME_STATUS_WRITING &&
          <div>
            <div className="option-buttons-container">
              {this.props.options.map((word, index) => {
                const onClick = () => this.onWordButtonClicked(index);
                const ref = (ref) => this.buttons[index] = ref;
                return <button className="option-button" key={index} onClick={onClick} ref={ref}>{word}</button>
              })}
            </div>
            <TimerBar wordNum={this.props.wordNum} countdownSecs={wordChoiceTime} className="word-timer-bar" />
          </div>
        }
      </div>
    );
  }
}

export default SentenceDisplay;
