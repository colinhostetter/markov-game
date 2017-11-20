import * as React from "react";
import SentenceDisplay from "./SentenceDisplay";
import HeadlineInstructions from "./HeadlineInstructions";
import ScoreDisplay from "./ScoreDisplay";
import WordsLeftCounter from "./WordsLeftCounter";
import GuessTimer from "./GuessTimer";
import GuessResult from "./GuessResult";
import constants from "../constants";
import "./GameDisplay.css";

const GameDisplay = ({
  guessesCorrect,
  guessing,
  writing,
  sentences,
  round,
  wordNum,
  onWordChosen,
  onGuessMade,
  guessedIndex,
  status
}) => (
  <div className="game-container">
    <ScoreDisplay guessesCorrect={guessesCorrect} />
    <HeadlineInstructions guessing={guessing} writing={writing} round={round} />
    <div className="sentences-container padded-edges">
      {sentences.map((sentence, index) => {
        const sentenceProps = {
          ...sentence,
          writing,
          guessing,
          onWordChosen,
          wordNum,
          onGuessMade: () => onGuessMade(index),
          key: index,
          isGuessed: status === "reveal" && guessedIndex === index,
          status
        };
        return <SentenceDisplay {...sentenceProps} />
      })}
    </div>
    <div className="bottom-contexual-panel padded-edges">
      {status === constants.GAME_STATUS_WRITING && <WordsLeftCounter wordNum={wordNum} />}
      {status === constants.GAME_STATUS_GUESS_TIME && <GuessTimer guessing={guessing} />}
      {status === constants.GAME_STATUS_REVEAL && <GuessResult guessing={guessing} correct={guessesCorrect[round]} />}
    </div>
  </div>
);

export default GameDisplay;
