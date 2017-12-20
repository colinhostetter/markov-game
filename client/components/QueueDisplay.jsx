import * as React from "react";
import "./QueueDisplay.css";

const copyButtonTextInitial = "Copy to clipboard";
const copyButtonTextFeedback = "Copied!";

class QueueDisplay extends React.Component {
  constructor(props) {
    super(props);
    this.state = { copyButtonText: copyButtonTextInitial };
    this.timeouts = {};
  }
  get joinLink() {
    return `http://127.0.0.1:5000/game?id=${this.props.gameId}`;
  }
  handleCopyButtonClicked() {
    const ta = document.createElement("textarea");
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    ta.value = this.joinLink;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
    this.setState({ copyButtonText: copyButtonTextFeedback });
    const timeoutId = setTimeout(() => {
      this.setState({ copyButtonText: copyButtonTextInitial });
      delete this.timeouts[timeoutId];
    }, 3000);
    this.timeouts[timeoutId] = true;
  }
  componentWillUnmount() {
    for (let key in this.timeouts) {
      clearTimeout(key);
    }
  }
  render() {
    return (
      <div className="queue-display padded-edges">
        {this.props.gameId && (
          <div className="join-link-container">
            <p>Send this link to your friend:</p>
            <p className="join-link">{this.joinLink}</p>
            <button className="copy-btn" onClick={this.handleCopyButtonClicked.bind(this)}>
              {this.state.copyButtonText}
            </button>
          </div>
        )}
        <p>
          {!this.props.gameId && "Waiting for another player to join..."}
          {this.props.gameId && "Waiting for your friend to join..."}
        </p>
        <div className="queue-loader-container">
          <img className="loading-icon" src="/assets/icons/loading.png" />
        </div>
      </div>
    )
  }
}

export default QueueDisplay;
