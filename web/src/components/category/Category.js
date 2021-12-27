import React from 'react';
import './Category.css';

const Category = ({ data }) => {
    return (
        <div className="category">
            <p>{ data.name }</p>
        </div>
    );
}

export default Category;
