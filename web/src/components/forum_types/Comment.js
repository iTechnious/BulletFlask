import {
    Paper,
    CardContent,
    Grid,
    Typography,
    Accordion,
    AccordionSummary,
    AccordionDetails,
    LinearProgress
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import React, {useState} from 'react';
import { useTranslation } from 'react-i18next';
import Box from "@mui/material/Box";

const Comment = ({ data }) => {
    const { t } = useTranslation();
    const [subcomments, setSubcomments] = useState([]);

    const fetch_subcomments = (event, expanded) => {
        if (!expanded) {return}

        fetch('/api/content/get/?location=' + data.id)
            .then(res => res.json())
            .then(_data=>{setSubcomments(_data.contents)})
    }

    return (
        <Grid item>
            <Paper elevation={4} className="comment" sx={{ padding: '0px' }}>
                <CardContent sx={{padding: '5px 20px !important'}}>
                    <Typography variant="p" fontSize={"medium"}>{ data.content }</Typography>

                    <>
                    {
                        data["subcomments"] > 0 ?
                            <Accordion onChange={fetch_subcomments} disableGutters square>
                            <AccordionSummary sx={{paddingLeft: "1px"}}
                                expandIcon={<ExpandMoreIcon />}

                            >
                                <Typography>{`${data["subcomments"]} ${t('COMMENTS')}`}</Typography>
                            </AccordionSummary>
                            <AccordionDetails sx={{padding: "1px"}}>
                                {
                                    subcomments.length === 0 ? <Box sx={{ width: '100%' }}><LinearProgress /></Box>
                                        : subcomments.map((element, key) => {return( <Comment key={key} data={element} /> )})
                                }

                            </AccordionDetails>
                        </Accordion>
                        : null
                    }
                    </>

                </CardContent>
            </Paper>
        </Grid>
    );
}

export default Comment;