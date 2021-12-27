import React from 'react';
import './Thread.css';

const Thread = ({ data }) => {
    return (
        <div className="thread">
            <p>{ data.name }</p>
        </div>
    );
}

export default Thread;