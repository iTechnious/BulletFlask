import React from "react";
import "./thread.css"

class Thread extends React.Component {
    click() {
        this.props.renew.bind(this.props.that)(this.props.data.id);
    }

    render() { return (
        <div className="thread" onClick={this.click.bind(this)}>
            <p>{this.props.data.name}</p>
        </div>
    )}
};

export default Thread;
