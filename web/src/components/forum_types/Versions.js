import {CardContent, Fade, Grid, Link, Modal, Paper, Typography} from '@mui/material';
import React, {useContext, useEffect, useState} from 'react';
import { useTranslation } from 'react-i18next';
import { NavLink } from 'react-router-dom';
import Backdrop from '@mui/material/Backdrop';
import Box from "@mui/material/Box";
import {LocationContext} from "../../pages/Forum";

const Versions = ({ data }) => {
    const { t } = useTranslation();

    const [versions, setVersions] = useState([]);
    const [modalOpen, setModalOpen] = useState(false);
    const {preDefVersion} = useContext(LocationContext);

    const getVersions = () => {
        fetch('/api/content/versions/?location=' + data.id, {
            credentials: 'include'
        })
        .then(res => res.json())
        .then(data => {
            setVersions(data);
        })
    }

    useEffect(getVersions, [data]);

    return (
        <>
            {
                versions.length > 0 ?
                    <p style={{fontStyle: "italic"}}>
                        <Link style={{cursor: "pointer"}} onClick={()=>{setModalOpen(true)}}>
                            {t('OTHER_VERSIONS_AVAIL', {amount: versions.length})}<br/>
                            {preDefVersion !== undefined ? <Typography color="error.main">{t('VERSION_ID', {id: preDefVersion})} {t('CHOOSEN')}</Typography> : null}
                        </Link>
                    </p> : null
            }

            <Modal open={modalOpen}
                   onClose={()=>{setModalOpen(false)}}
                   closeAfterTransition
                   BackdropComponent={Backdrop}
                   BackdropProps={{
                      timeout: 500,
                   }}>
                <Fade in={modalOpen}>
                    <Box sx={{
                        position: 'absolute',
                        top: '50%',
                        left: '50%',
                        transform: 'translate(-50%, -50%)',
                        width: 400,
                        bgcolor: 'background.paper',
                        border: '2px solid',
                        boxShadow: 24,
                        p: 4,
                        maxHeight: "70vh",
                        overflow: "auto",
                        minWidth: "60vw"
                    }}>
                        <Typography>{t('CHILDS_NOT_AFFECTED')}</Typography>
                        <Grid container
                              direction={"column"}
                              rowSpacing={1}
                              justifyContent={"center"}>
                        {
                            preDefVersion !== undefined ?
                                <Grid item>
                                    <NavLink to={`/forum/${data.id}`} style={{textDecoration: "none"}} onClick={()=>{setModalOpen(false)}}>
                                        <Paper elevation={5} className="thread" sx={{ padding: '5px'}} style={ {cursor: "pointer"} }>
                                            <CardContent style={{padding: "16px"}}>
                                                <Typography variant="h5">{t('CURRENT_VERSION')}</Typography>
                                            </CardContent>
                                        </Paper>
                                    </NavLink>
                                </Grid> : null
                        }

                        {
                            versions.map((value, index)=> {
                                return (
                                    <Grid item key={index}>
                                        <NavLink to={`/forum/${data.id}/${value.id}`} style={{textDecoration: "none"}} onClick={()=>{setModalOpen(false)}}>
                                            <Paper elevation={5} className="thread" sx={{ padding: '5px'}} style={ {cursor: "pointer"} }>
                                                <CardContent style={{padding: "16px"}}>
                                                    <Typography gutterBottom color="text.secondary">{t('VERSION_ID', {id: value.id})}</Typography>
                                                    <Typography>{value.date}</Typography>
                                                    {value.id.toString() === preDefVersion ?
                                                        <Typography gutterBottom
                                                                    color="error.main"
                                                                    style={{fontStyle: "italic", margin: "0"}}>
                                                            {t('CHOOSEN')}
                                                        </Typography> : null }
                                                </CardContent>
                                            </Paper>
                                        </NavLink>
                                    </Grid>
                                );
                            })
                        }
                        </Grid>
                    </Box>
                </Fade>
            </Modal>
        </>
    );
}

export default Versions;