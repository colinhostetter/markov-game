import * as React from "react";
import "./DisconnectedAlert.css";

class DisconnectedAlert extends React.Component {
  render() {
    if (this.props.connected && this.props.partnerConnected) {
      return null;
    }

    let message;
    if (!this.props.connected) {
      message = "Lost connection to server; will try to reconnect...";
    } else if (!this.props.partnerConnected) {
      message = "Your partner has disconnected :(";
    }
    return (
      <div className="disconnected-alert">
        {message}
      </div>
    )
  }
}

export default DisconnectedAlert;
