import React from "react";
import "./thread.css"

class Thread extends React.Component {
    render() { return (
        <div className="thread">
            <p>{this.props.data.name}</p>
        </div>
    )}
};

export default Thread;
