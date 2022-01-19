import { Avatar, Button, Checkbox, Link, FormControlLabel, Grid, TextField, Typography, CssBaseline, Container, CircularProgress, Alert } from '@mui/material';
import { Lock as LockIcon } from '@mui/icons-material';
import React, {useContext, useState} from 'react';
import { Box } from '@mui/system';
import { UserContext } from '../index';
import { useTranslation } from 'react-i18next';
import { Link as RouterLink } from "react-router-dom";

const Register = () => {
    const { t } = useTranslation();

    // Grab user states from global states.
    const { loggedIn, pending, setLoggedIn, setPending, setUser } = useContext(UserContext);

    // Error/message returned by the API.
    const [error, setError] = useState('');

    const handleRegistrationAttempt = (event) => {
        setPending(true);
        
        fetch('/register/', {
            method: 'POST',
            body: new FormData(event.currentTarget)
        })
        .then(res => {
            if (res.status === 200) {
                setUser(res.user);
                setLoggedIn(true);
            } else {
                setError(res.error);
            }

            setPending(false);
        })
    };

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
                    { t('SIGN_UP') }
                </Typography>

                <Box component="form" onSubmit={ handleRegistrationAttempt } noValidate sx={{ mt: 1 }}>
                    { loggedIn && <Alert severity="success">{ t('LOGIN_SUCCEEDED') }</Alert> }
                    { error !== '' && <Alert severity="error">{ `${ t('ERROR') }: ${ t(error["frontend"], { ns:"errors" }) }` }</Alert> }
                    
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="username"
                        label={ t('USERNAME') }
                        type="text"
                        id="username"
                    />

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
                        { t('SIGN_UP') }
                    </Button>

                    <Grid container>
                        <Grid item xs>
                            <Link href="#" variant="body2">
                                { t('FORGOT_PASSWORD') }
                            </Link>
                        </Grid>
                        <Grid item>
                            <Link component={ RouterLink } to="/login" variant="body2">
                            { t('SIGN_IN') }
                            </Link>
                        </Grid>
                    </Grid>
                </Box>
            </Box>
        </Container>
        </>
    );
}

export default Register;
