import { Avatar, Button, Checkbox, Link, FormControlLabel, Grid, TextField, Typography, CssBaseline, Container, CircularProgress, Alert } from '@mui/material';
import { Lock as LockIcon } from '@mui/icons-material';
import React, { useContext, useEffect, useState } from 'react';
import { Box } from '@mui/system';
import { UserContext } from '../context/UserContext';
import { useTranslation } from 'react-i18next';

const Register = () => {
    const { t } = useTranslation();

    // Grab user states from global states.
    const { loggedIn, pending, setLoggedIn, setPending, setUser } = useContext(UserContext);

    // Error/message returned by the API.
    const [error, setError] = useState('');

    const handleRegistrationAttempt = () => {

    };

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
                    { error !== '' && <Alert severity="error">{ `${ t('ERROR') }: ${ t(error.code, { ns:"errors" }) }` }</Alert> }
                    
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

                    <FormControlLabel
                        control={<Checkbox value="remember" color="primary" />}
                        label="Remember me"
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
                            <Link href="#" variant="body2">
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

export default Register;
