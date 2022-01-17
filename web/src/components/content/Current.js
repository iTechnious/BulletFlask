import { Typography } from "@mui/material";
import React from "react";
import ReactMarkdown from 'react-markdown';
import SyntaxHighlighter from "react-syntax-highlighter/dist/cjs/light";


const Current = ( {data} ) => {
    return (
        <div id={"forum-current"}>
            <Typography variant="h3" sx={{ margin: '30px 0 30px 0' }}>{ data.name }</Typography>
            <Typography>
                <ReactMarkdown
                    children={data.content}
                />
            </Typography>
        </div>
    )
};

export default Current;
