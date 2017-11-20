import React from "react";
import ReactDOM from "react-dom";
import io from "socket.io-client";
import uuidv4 from 'uuid';
import GameContainer from "./components/GameContainer";
import constants from "./constants.js";

import "./app.css";

// User IDs have no value other than allowing reconnection, so let's just
// generate it here and declare ourselves to the server.
const cookieExists = document.cookie.includes(`${constants.COOKIE_NAME}=`);
if (!cookieExists) {
  const user_id = uuidv4();
  document.cookie = `${constants.COOKIE_NAME}=${user_id}`;
}

const socket = io.connect();
socket.on("connect", () => {
  // temp until I add queueing stuff
  socket.emit("join_game", {"game_id": "a"});
});

ReactDOM.render(<GameContainer socket={socket} />, document.getElementById("app"));
