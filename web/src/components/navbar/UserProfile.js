import { AccountCircle, Logout } from '@mui/icons-material';
import { Button, Divider, IconButton, Link, ListItemIcon, ListItemText, Menu, MenuItem } from '@mui/material';
import { t } from 'i18next';
import React, { useContext, useState } from 'react';
import { UserContext } from '../../index';

const UserProfile = () => {
    // Get user-specific states from global user context.
    const { loggedIn, user, setLoggedIn, setUser } = useContext(UserContext);

    const [anchorEl, setAnchorEl] = useState(null);
  
    const handleMenu = (event) => {
      setAnchorEl(event.currentTarget);
    };
  
    const handleClose = () => {
      setAnchorEl(null);
    };

    const handleLogout = () => {
        fetch('/logout/')
        .then(res => {
            if(res.status === 200) {
                setLoggedIn(false);
                setUser({});
            } else {
                alert('An error occurred! Please try again later.');
            }
        });
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
                anchorEl={ anchorEl }
                anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                }}
                keepMounted
                transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                }}
                open={ Boolean(anchorEl) }
                onClose={ handleClose }
                PaperProps={{  
                    style: {  
                      width: 200,  
                    },
                }}
            >
                <MenuItem onClick={ handleClose }>
                    <ListItemIcon>
                        <AccountCircle />
                    </ListItemIcon>
                    
                    <ListItemText>{ user.username }</ListItemText>
                </MenuItem>
                
                <Divider />

                <MenuItem onClick={ handleLogout }>
                    <ListItemIcon>
                        <Logout />
                    </ListItemIcon>
                    
                    <ListItemText>{ t('SIGN_OUT') }</ListItemText>
                </MenuItem>
            </Menu>
      </div>
    );
}

export default UserProfile;
