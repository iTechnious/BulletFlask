import React from 'react';

import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { t } from "i18next";
import { Link } from 'react-router-dom';

const Navbar = () => {
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

            {/* TODO: Check if user is already signed in. */}
            <Button to="/login" color="inherit" component={ Link }>{ t('SIGN_IN') }</Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}

export default Navbar;