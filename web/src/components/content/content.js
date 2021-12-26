import React from "react";
import Thread from "../thread/thread";
import Category from "../category/category";

class Content extends React.Component {
    render() { return (
        <>
        {
            this.props.data.map(ele => {
                if(ele.type === "thread") {
                    return(<Thread data={ele} renew={this.props.renew} that={this.props.that} />)
                }
            })
        }
        {
            this.props.data.map(ele => {
                if(ele.type === "category") {
                    return(<Category data={ele} renew={this.props.renew} that={this.props.that} />)
                }
            })
        }
        </>
    )}
};

export default Content;
