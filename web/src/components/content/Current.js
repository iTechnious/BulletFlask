import React from "react";

const Current = ( {data} ) => {
    return (
        <>
            <h1>{data.name}</h1>
            <p>{data.content}</p>
        </>
    )
};

export default Current;
