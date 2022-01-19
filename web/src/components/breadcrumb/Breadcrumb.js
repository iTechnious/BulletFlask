import Breadcrumbs from '@mui/material/Breadcrumbs';
import Link from '@mui/material/Link';
import React from "react";
import {NavLink} from "react-router-dom";

const Breadcrumb = ( {data, renew} ) => {
    return (
        <div role="presentation">
            <Breadcrumbs aria-label="breadcrumb">
                {
                    data.map((ele, i)=>{
                        return(
                            <NavLink key={i}
                                     to={`/forum/${ele !== undefined ? ele.id : "0"}`}
                                     style={{textDecoration: "none"}}
                                     underline="hover">
                                <Link>{ ele.name }</Link>
                            </NavLink>
                        )
                    })
                }
            </Breadcrumbs>
        </div>
    )
};

export default Breadcrumb;
