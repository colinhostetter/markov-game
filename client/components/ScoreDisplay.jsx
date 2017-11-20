import * as React from "react";
import classNames from "classnames";
import constants from "../constants";
import "./ScoreDisplay.css";

const ScoreDisplay = ({ guessesCorrect }) => {
  const displays = Array(constants.ROUNDS_PER_GAME).fill({});
  guessesCorrect.forEach((correct, index) => {
    displays[index] = correct ? {cls: "correct", icon: "✔"} : {cls: "incorrect", icon: "❌"};
  });
  return (
    <div className="score-display">
      <div className="score-horizontal-line" />
      <div className="score-icons-container">
        {displays.map(({ cls, icon }, index) => {
          return (
            <div className={classNames("round-result-circle", cls)} key={index}>
              <div className="icon">{icon}</div>
              <div className="coverup"></div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ScoreDisplay;
