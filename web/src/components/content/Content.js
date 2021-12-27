import React from 'react';
import Thread from '../thread/thread';
import Category from '../category/Category';

const Content = ({ data }) => {
    return (
        data.map((element, index) => {
            if (element.type === 'thread') {
                return <Thread key={ index } data={ element } />
            }

            if (element.type === 'category') {
                return <Category key={ index } data={ element } />
            }
        })
    );
}

export default Content;
