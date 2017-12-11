import * as React from "react";
import GameContainer from "./GameContainer";
import PostGameDisplay from "./PostGameDisplay";
import QueueDisplay from "./QueueDisplay";
import constants from "../constants";

class MarkovsRevenge extends React.Component {
  constructor(props) {
    super(props);
    this.state = { inGame: false, queued: this.props.queued, gameId: this.props.gameId };
    
    const socket = this.props.socket;
    socket.on("game_ready", ({ game_id }) => {
      this.setState({ gameId: game_id });
      socket.emit("join_game", { game_id })
    });
    socket.on("game_starting", () => {
      this.setState({ inGame: true, queued: false });
    });
    socket.on("game_ended", ({ game_id, guesses_correct }) => {
      if (game_id === this.state.gameId) {
        this.setState({ inGame: false, postGame: true, guessesCorrect: guesses_correct });
      }
    })

    setInterval(() => {
      if (this.state.queued) {
        socket.emit("heartbeat", { queue: true });
      } else if (this.state.gameId && !this.state.inGame) {
        socket.emit("heartbeat", { game_id: this.state.gameId });
      }
    }, 1000);
  }
  render() {
    if (this.state.inGame) {
      return <GameContainer socket={this.props.socket} gameId={this.state.gameId} />
    } else if (this.state.postGame) {
      return <PostGameDisplay guessesCorrect={this.state.guessesCorrect} />
    } else {
      return <QueueDisplay gameId={this.props.gameId} />
    }
  }
}

export default MarkovsRevenge;
