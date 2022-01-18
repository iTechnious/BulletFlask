import Breadcrumbs from '@mui/material/Breadcrumbs';
import Link from '@mui/material/Link';
import React from "react";

const Breadcrumb = ( {data, renew} ) => {
    return (
        <div role="presentation">
            <Breadcrumbs aria-label="breadcrumb">
                {
                    data.map((ele, i)=>{
                        return(
                            <Link key={i} underline="hover" style={ {cursor: "pointer"} } onClick={ ()=>{ renew(ele.id) } }>
                                { ele.name }
                            </Link>
                        )
                    })
                }
            </Breadcrumbs>
        </div>
    )
};

export default Breadcrumb;
