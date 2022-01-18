import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import Slide from '@mui/material/Slide';
import {IconButton} from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';


const ErrorBox = ( {message, setMessage, severity} ) => {
    return (
        <Slide direction="left" in={message !== undefined && severity !== undefined} mountOnEnter unmountOnExit>
        <Box sx={{ width: '50%' }} position={"absolute"} top={"70px"} right={"10px"}>

            <Alert action=
                       {
                           <IconButton
                                aria-label="close"
                                color="inherit"
                                size="small"
                                onClick={() => {
                                    setMessage({});
                                }}>
                                <CloseIcon fontSize="inherit"/>
                           </IconButton>
                       }
                   severity={severity}
            >
                {message}
            </Alert>
        </Box>
        </Slide>
    );
}

export default ErrorBox;