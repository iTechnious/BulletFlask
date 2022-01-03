import { Avatar, Button, Link, Grid, TextField, Typography, CssBaseline, Container, CircularProgress, Alert } from '@mui/material';
import { Lock as LockIcon } from '@mui/icons-material';
import React, { useContext, useEffect, useState } from 'react';
import { Box } from '@mui/system';
import { UserContext } from '../context/UserContext';
import { useTranslation } from 'react-i18next';
import { Link as RouterLink } from 'react-router-dom';


/**
 * Login component.
 *
 * Heavily inspired by
 * https://github.com/mui-org/material-ui/blob/master/docs/src/pages/getting-started/templates/sign-in/SignIn.js.
 */
const Login = () => {
    // Grab user states from global states.
    const { loggedIn, pending, setLoggedIn, setPending, setUser } = useContext(UserContext);

    const { t } = useTranslation();

    // Error/message returned by the API.
    const [error, setError] = useState('');
    
    const handleLoginAttempt = (event) => {
        // Prevent browser for submission redirect.
        event.preventDefault();

        // Construct FormData from values in the form.
        var formData = new FormData(event.currentTarget);
        
        // TODO: Remove hard-coded login request and replace with login form.
        fetch('/login/', {
            method: 'POST',
            credentials: 'include',
            body: formData
        })
        .then(res => {
            if (res.status === 200 || res.status === 202) {
                setLoggedIn(true);
                res.json().then(res => setUser(res["user"]));
                setPending(false);
            } else {
                res.json().then(res => {
                    if (res["error"]) setError(res["error"]);
                    else setError('An unknown error occurred! Please try again later.');
                });
                setLoggedIn(false);
                setPending(false);
            }
            setPending(false);
        });
    }
    
    if (loggedIn) {
        // TODO: Readirect using react-router!!!
        window.location.replace('/forum');
    }

    return (
        <>
        <Container component="main" maxWidth="xs">
            <CssBaseline />
            <Box
            sx={{
                marginTop: 8,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
            }}
            >
                <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                    <LockIcon />
                </Avatar>

                <Typography component="h1" variant="h5">
                    { t('SIGN_IN') }
                </Typography>

                <Box component="form" onSubmit={ handleLoginAttempt } noValidate sx={{ mt: 1 }}>
                    { error !== '' && <Alert severity="error">{ `${ t('ERROR') }: ${ t(error["frontend"], { ns:"errors" }) }` }</Alert> }
                    
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        id="email"
                        label={ t('EMAIL_ADDRESS') }
                        name="email"
                        autoComplete="email"
                        autoFocus
                    />

                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="password"
                        label={ t('PASSWORD') }
                        type="password"
                        id="password"
                        autoComplete="current-password"
                    />

                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        disabled={ pending }
                        sx={{ mt: 3, mb: 2 }}
                    >
                        { pending && <CircularProgress /> }
                        { t('SIGN_IN') }
                    </Button>

                    <Grid container>
                        <Grid item xs>
                            <Link href="#" variant="body2">
                                { t('FORGOT_PASSWORD') }
                            </Link>
                        </Grid>
                        <Grid item>
                            <Link component={ RouterLink } to="/register" variant="body2">
                            { t('DONT_HAVE_ACC_SIGN_UP') }
                            </Link>
                        </Grid>
                    </Grid>
                </Box>
            </Box>
        </Container>
        </>
    );
}

export default Login;
