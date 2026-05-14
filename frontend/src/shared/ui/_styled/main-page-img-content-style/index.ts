import { styled } from "@mui/material";

export const MainPageImgContentStyled = styled("div")(({ theme }) => ({
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  maxWidth: "1280px",
  width: "100%",
  height: "100%",
  gap: theme.spacing(1.5),
  paddingInline: theme.spacing(2),
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",

  [theme.breakpoints.up("sm")]: {
    paddingInline: theme.spacing(3),
  },
}));
