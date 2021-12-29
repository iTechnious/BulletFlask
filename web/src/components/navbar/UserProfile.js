import { AccountCircle } from '@mui/icons-material';
import { Button, IconButton, Link, Menu, MenuItem } from '@mui/material';
import { t } from 'i18next';
import React, { useContext, useState } from 'react';
import { UserContext } from '../../context/UserContext';

const UserProfile = () => {
    // Get user-specific states from global user context.
    const { loggedIn } = useContext(UserContext);

    const [anchorEl, setAnchorEl] = useState(null);
  
    const handleMenu = (event) => {
      setAnchorEl(event.currentTarget);
    };
  
    const handleClose = () => {
      setAnchorEl(null);
    };

    // Return "Sign in" button if user is not signed in.
    if (!loggedIn) {
        return <Button to="/login" color="inherit" component={ Link }>{ t('SIGN_IN') }</Button>;
    }

    return (
        <div>
            <IconButton
                size="large"
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={ handleMenu }
                color="inherit"
            >
                {/* TODO: Show user profile picture. */}
                <AccountCircle />
            </IconButton>
            <Menu
                id="menu-appbar"
                anchorEl={anchorEl}
                anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                }}
                keepMounted
                transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                }}
                open={Boolean(anchorEl)}
                onClose={ handleClose }
            >
                <MenuItem onClick={ handleClose }>{ t('PROFILE') }</MenuItem>
                {/* TODO: Make logout work. */}
                <MenuItem onClick={ handleClose }>{ t('SIGN_OUT') }</MenuItem>
            </Menu>
      </div>
    );
}

export default UserProfile;
