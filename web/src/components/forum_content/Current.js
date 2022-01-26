import { Typography } from "@mui/material";
import React from "react";
import ReactMarkdown from 'react-markdown';
import Versions from "../forum_types/Versions";

const Current = ( {data} ) => {
    return (
        <div id={"forum-current"}>
            {data.type === "thread" ? <Versions data={data} /> : null}

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
