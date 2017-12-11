import * as React from "react";
import GameDisplay from "./GameDisplay";
import constants from "../constants";

export default class GameContainer extends React.Component {
  constructor({ socket }) {
    super();
    // temp state which will be replaced by the server soon
    this.state = {
      connected: true,
      partnerConnected: true,
      guessesCorrect: [],
      guessing: true,
      round: 0,
      sentences: [],
      wordNum: 0,
      writing: false
    };
    socket.on("game_state", gameState => {
      if (gameState.game_id === this.props.gameId) {
        this.setState({
          connected: true,
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
        this.lastServerHeartbeat = Date.now();
      }
    });
    socket.on("guess_made", guess => {
      this.setState({
        guessedIndex: guess.sentence_index,
        guessedCorrect: guess.correct
      })
    });
    this.heartbeatIntervalId = setInterval(this.heartbeat.bind(this), constants.HEARTBEAT_INTERVAL_SECONDS * 1000);
    this.lastServerHeartbeat = Date.now();
    socket.on("heartbeat", () => this.lastServerHeartbeat = Date.now());
    socket.on("partner_inactive", ({ game_id }) => {
      if (game_id === this.props.gameId) this.setState({ partnerConnected: false });
    });
  }
  heartbeat() {
    this.props.socket.emit("heartbeat", {game_id: this.props.gameId});
    if (Date.now() - this.lastServerHeartbeat > 3000) {
      this.setState({ connected: false });
    }
  }
  handleWordChosen(index) {
    if (this.state.writing) {
      this.props.socket.emit("choose_word", {
        word_index: index,
        word_num: this.state.wordNum,
        game_id: this.props.gameId
      });
    }
  }
  handleGuessMade(index) {
    if (this.state.guessing) {
      this.props.socket.emit("guess_sentence", {
        sentence_index: index,
        round: this.state.round,
        game_id: this.props.gameId
      })
    }
  }
  componentWillUnmount() {
    clearInterval(this.heartbeatIntervalId);
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
