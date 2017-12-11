import React from "react";
import ReactDOM from "react-dom";
import io from "socket.io-client";
import uuidv4 from "uuid";
import url from "url";
import MarkovsRevenge from "./components/MarkovsRevenge";
import constants from "./constants.js";
import "./app.css";

const appContainer = document.getElementById("app");
appContainer.setAttribute("data-running", "1");

// Remove loader
const loader = document.getElementById("load");
document.body.removeChild(loader);

// User IDs have no value other than allowing reconnection, so let's just
// generate it here and declare ourselves to the server.
const cookieExists = document.cookie.includes(`${constants.COOKIE_NAME}=`);
if (!cookieExists) {
  const userId = uuidv4();
  document.cookie = `${constants.COOKIE_NAME}=${userId}`;
}

const socket = io.connect();
socket.on("connect", () => {
  const props = { socket };

  const parsed = url.parse(window.location.href, true);
  if (parsed.query.id) {
    socket.emit("join_game", {game_id: parsed.query.id});
    props.gameId = parsed.query.id;
  } else if (parsed.query.mode === "wait") {
    const gameId = uuidv4();
    socket.emit("join_game", {game_id: gameId});
    props.gameId = gameId;
  } else {
    socket.emit("join_queue");
    props.queued = true;
  }

  ReactDOM.render(<MarkovsRevenge {...props} />, appContainer);
});
