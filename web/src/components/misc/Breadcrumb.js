import Breadcrumbs from '@mui/material/Breadcrumbs';
import Link from '@mui/material/Link';
import React from "react";
import {NavLink} from "react-router-dom";
import {useTheme} from "@mui/material/styles";
import {Slide, Typography, useScrollTrigger} from "@mui/material";

const Breadcrumb = ( {data} ) => {
    const theme = useTheme();

    const show = useScrollTrigger({
        target: React.window ? React.window() : undefined,
    });

    return (
        <Slide in={!show} appear={true}>
            <div role="presentation" style={{backgroundColor: theme.palette.background.paper}}>
                <Breadcrumbs aria-label="breadcrumb" style={{padding: "5px 10px"}}>
                    {
                        data.map((ele, i)=>{
                            return(
                                <NavLink key={i}
                                         to={`/forum/${ele !== undefined ? ele.id : "0"}`}
                                         style={{textDecoration: "none"}}>
                                    <Typography component="p"
                                            fontSize="large"
                                            style={{
                                                textDecoration: "none",
                                                color: theme.palette.text.primary
                                            }}>
                                        <Link
                                            underline="hover"
                                            color="inherit">
                                            { ele.name }
                                        </Link>
                                    </Typography>
                                </NavLink>
                            )
                        })
                    }
                </Breadcrumbs>
            </div>
        </Slide>

    )
};

export default Breadcrumb;
