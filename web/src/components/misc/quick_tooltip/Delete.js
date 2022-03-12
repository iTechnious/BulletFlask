import {useTranslation} from "react-i18next";
import Backdrop from "@mui/material/Backdrop";
import {CardContent, Fade, Grid, Modal, Paper, Typography} from "@mui/material";
import Box from "@mui/material/Box";
import {NavLink} from "react-router-dom";
import React, {useState} from "react";


export const DeleteModal = ({open, setOpen}) => {
    const { t } = useTranslation();

    return(
        <>
        <Modal open={open}
               onClose={()=>{setOpen(false)}}
               closeAfterTransition
               BackdropComponent={Backdrop}
               BackdropProps={{
                  timeout: 500,
               }}>
            <Fade in={open}>
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
                    <Typography>löschen</Typography>
                </Box>
            </Fade>
        </Modal>
        </>
    )
}
