import * as React from "react";
import GameDisplay from "./GameDisplay";

export default class GameContainer extends React.Component {
  constructor({ socket }) {
    super();
    // temp state which will be replaced by the server soon
    this.state = {
      gameId: null,
      guessesCorrect: [],
      guessing: true,
      round: 0,
      sentences: [],
      wordNum: 0,
      writing: false
    };
    socket.on("game_state", gameState => {
      this.setState({
        gameId: gameState.game_id,
        guessesCorrect: gameState.guesses_correct,
        guessing: gameState.guessing,
        round: gameState.round,
        sentences: gameState.sentences.map(s => {
          return { words: s.words, isPlayer: s.is_player, options: s.options }
        }),
        status: gameState.status,
        wordNum: gameState.word_num,
        writing: gameState.writing
      });
    });
    socket.on("guess_made", guess => {
      this.setState({
        guessedIndex: guess.sentence_index
      })
    })
  }
  handleWordChosen(index) {
    if (this.state.writing) {
      this.props.socket.emit("choose_word", {
        word_index: index,
        word_num: this.state.wordNum,
        game_id: this.state.gameId
      });
    }
  }
  handleGuessMade(index) {
    if (this.state.guessing) {
      this.props.socket.emit("guess_sentence", {
        sentence_index: index,
        round: this.state.round,
        game_id: this.state.gameId
      })
    }
  }
  render() {
    const gameDisplayProps = {
      ...this.state,
      onWordChosen: this.handleWordChosen.bind(this),
      onGuessMade: this.handleGuessMade.bind(this)
    };
    return <GameDisplay {...gameDisplayProps} />;
  }
};
