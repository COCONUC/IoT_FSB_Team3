/* eslint-disable react-hooks/exhaustive-deps */
import axios from "axios";
import React, { useEffect, useState } from "react";
import { IconButton, Snackbar } from "@mui/material";

interface Props {
  temp: string;
  humid: string;
}

export default function Alarm(props: Props) {
  const [open, setOpen] = React.useState(false);
  const [snackbarMess, setSnackbarMess] = useState("");
  const [successMess, setSuccessMess] = useState("");
  const [errorMess, setErrorMess] = useState("");
  const [snackbarColor, setSnackbarColor] = useState("");

  const getValidation = async () => {
    try {
      console.log(`http://localhost:5000/api/validate?temp=${props.temp}&humid=${props.humid}`);
      const res = await axios.get(`http://localhost:5000/api/validate?temp=${props.temp}&humid=${props.humid}`);
      if (res.status === 200)
        if (res.data.message) {
          setSuccessMess(
            `✓  With temperature ${props.temp}°C and ${props.humid}% humidity, it is safety to live in this environment`
          );
          setSnackbarColor("#5acc3d");
        } else {
          setSuccessMess(
            `X  With temperature ${props.temp}°C and ${props.humid}% humidity, it is not healthy to live in this environment`
          );
          setSnackbarColor("#FF0000");
        }
    } catch (error) {
      setErrorMess("Failed to validate temperature and humidity!!!");
    }
  };

  const handleClose = (_event: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === "clickaway") return;
    setOpen(false);
  };

  useEffect(() => {
    getValidation();
  }, []);

  useEffect(() => {
    if (successMess.length > 0) setSnackbarMess(successMess);
  }, [successMess]);

  useEffect(() => {
    if (errorMess.length > 0) setSnackbarMess(errorMess);
  }, [errorMess]);

  useEffect(() => {
    if (snackbarMess.length > 0) setOpen(true);
  }, [snackbarMess]);

  const action = (
    <React.Fragment>
      <IconButton size="small" aria-label="close" color="inherit" onClick={handleClose}>
        X
      </IconButton>
    </React.Fragment>
  );

  return (
    <div>
      {open && snackbarMess && (
        <Snackbar
          style={{ background: snackbarColor, color: snackbarColor }}
          open={open}
          autoHideDuration={10000}
          onClose={handleClose}
          message={snackbarMess}
          action={action}
          anchorOrigin={{ vertical: "top", horizontal: "right" }}
        />
      )}
    </div>
  );
}
