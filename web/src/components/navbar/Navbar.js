import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import UserProfile from './UserProfile';
import CustomCircularProgress from "../Progress"
import {Fade} from "@mui/material";


const Navbar = ( {IsLoading} ) => {
    return (
        <Box sx={{ flexGrow: 1 }}>
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