import * as React from "react";
import classNames from "classnames";
import constants from "../constants";
import "./ScoreDisplay.css";

const ScoreDisplay = ({ guessesCorrect }) => {
  const displays = Array(constants.ROUNDS_PER_GAME).fill(null);
  guessesCorrect.forEach((correct, index) => {
    displays[index] = correct ? "check" : "x";
  });
  return (
    <div className="score-display">
      <div className="score-horizontal-line" />
      <div className="score-icons-container">
        {displays.map((icon, index) => {
          return (
            <div className={classNames("round-result-circle", icon && "filled")} key={index}>
              {icon && <img className="icon" src={`/assets/icons/${icon}.png`} />}
              <div className="coverup"></div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ScoreDisplay;
