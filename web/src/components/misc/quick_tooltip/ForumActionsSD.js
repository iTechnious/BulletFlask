import React, {useState} from 'react';
import SpeedDial from '@mui/material/SpeedDial';
import SpeedDialAction from '@mui/material/SpeedDialAction';
import {useTranslation} from "react-i18next";
import {ContentCopy, ContentPaste, Delete, Edit} from "@mui/icons-material";
import {SpeedDialIcon} from "@mui/material";
import {DeleteModal} from "./Delete";


const ForumActionSD = () => {
    const { t } = useTranslation();

    const [deleteOpen, setDeleteOpen] = useState(false);

    const actions = [
        { icon: <ContentPaste />, name: t("PASTE") },
        { icon: <ContentCopy />, name: t("CUT") },
        { icon: <Delete />, name: t("DELETE"), action: ()=>setDeleteOpen(true) },
        { icon: <Edit />, name: t("EDIT") },
    ];

    return (
        <>
            <DeleteModal open={deleteOpen} setOpen={setDeleteOpen} />
            <SpeedDial
                sx={{ position: 'fixed', bottom: 16, right: 16 }}
                icon={<SpeedDialIcon />}
                ariaLabel={"forum-actions"}>
                {actions.map((action) => (
                    <SpeedDialAction
                        key={action.name}
                        icon={action.icon}
                        tooltipTitle={action.name}
                        onClick={action.action}
                    />
                ))}
            </SpeedDial>
        </>

    );
}

export default ForumActionSD;
