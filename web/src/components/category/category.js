import React from "react";
import "./category.css"

class Category extends React.Component {
    click() {
        this.props.renew.bind(this.props.that)(this.props.data.id);
    }
    render() {
    return (
        <div className="category" onClick={this.click.bind(this)}>
            <p>{this.props.data.name}</p>
        </div>
    )}
};

export default Category;
