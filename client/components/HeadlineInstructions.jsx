import * as React from "react";
import "./HeadlineInstructions.css";

const HeadlineInstructions = ({ writing, guessing, round }) => {
  let headline, hint;
  if (round === 0) {
    headline = writing ? "You're writing first!" : "You're guessing first!";
  } else {
    headline = writing ? "Your turn to write!" : "Your turn to guess!";
  }
  hint = writing ? "Create a sentence your partner will recognize as human-written" :
                   "Guess which sentence is being written by your partner";
  return (
    <div className="headline-instructions-container padded-edges">
      <h2>{headline}</h2>
      <aside>{hint}</aside>
    </div>
  )
}

export default HeadlineInstructions;
