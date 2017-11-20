import * as React from "react";
import classnames from "classnames";
import "./GuessResult.css";

const GuessResult = ({ guessing, correct }) => {
  return (
    <div className="guess-result">
      <div className={classnames("guess-result-icon-container", correct ? "correct" : "incorrect")}>
        <div className="guess-result-icon">{correct ? "✔" : "❌"}</div>
      </div>
      <div className="guess-result-text">
        {guessing ? "You" : "Your partner"} guessed {correct ? "correctly" : "incorrectly"}!
      </div>
    </div>
  )
}

export default GuessResult;
