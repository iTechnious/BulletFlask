import { Typography } from "@mui/material";
import React from "react";

const Current = ( {data} ) => {
    return (
        <>
            <Typography variant="h3" sx={{ margin: '30px 0 30px 0' }}>{ data.name }</Typography>
            <p>{data.content}</p>
        </>
    )
};

export default Current;
