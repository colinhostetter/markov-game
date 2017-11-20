import * as React from "react";
import constants from "../constants";
import "./WordsLeftCounter.css";

const WordsLeftCounter = ({ wordNum }) => {
  const wordsLeft = constants.WORDS_PER_SENTENCE - wordNum;
  return <div className="words-left-counter">{wordsLeft} {wordsLeft === 1 ? "word": "words"} left!</div>;
}

export default WordsLeftCounter;
