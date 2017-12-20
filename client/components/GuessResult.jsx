import * as React from "react";
import classnames from "classnames";
import "./GuessResult.css";

const GuessResult = ({ guessing, correct }) => {
  let text = guessing ? "You " : "Your partner ";
  if (correct === true) {
    text += "guessed correctly!";
  } else if (correct === false) {
    text += "guessed incorrectly!";
  } else {
    text += "didn't guess!";
    if (guessing) {
      text += " Next time, guess before time runs out!";
    }
  }
  const iconPath = `/assets/icons/${correct ? "check" : "x"}.png`
  return (
    <div className="guess-result">
      <div className="guess-result-icon-container">
        <img className="guess-result-icon" src={iconPath} />
      </div>
      <div className="guess-result-text">
        {text}
      </div>
    </div>
  )
}

export default GuessResult;
