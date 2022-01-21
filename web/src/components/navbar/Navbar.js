import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import UserProfile from './UserProfile';
import CustomCircularProgress from "../Progress"
import {Fade, FormControlLabel, Switch} from "@mui/material";
import {useContext} from "react";
import {ColorModeContext} from "../../index";
import {useTranslation} from "react-i18next";


const Navbar = ( {IsLoading} ) => {
    const {colorMode, setColorMode} = useContext(ColorModeContext);
    const { t } = useTranslation();

    return (
        <Box sx={{ flexGrow: 1 }} zIndex={1000}>
        <AppBar position="static">
            <Toolbar>
                {/* <IconButton
                    size="large"
                    edge="start"
                    color="inherit"
                    aria-label="menu"
                    sx={{ mr: 2 }}
                >
                    <MenuIcon />
                </IconButton> */}
                <Typography variant="h5" component="div" sx={{ flexGrow: 1 }}>
                    {/* TODO: Replace with forum name of this instance. */}
                    BulletFlask
                </Typography>

                <FormControlLabel control={
                    <Switch checked={colorMode === "dark"} onChange={(event)=>{setColorMode(event.target.checked ? "dark" : "light")}} />
                } label={t('DARKMODE')} />

                <Fade in={IsLoading}>
                    <div>
                        <CustomCircularProgress/>
                    </div>
                </Fade>

                {/* TODO: Check if user is already signed in. */}
                <UserProfile />
            </Toolbar>
        </AppBar>
        </Box>
    );
}

export default Navbar;