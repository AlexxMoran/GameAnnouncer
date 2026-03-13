import { styled } from "@mui/material";

export const PageContentWrapperStyled = styled("div")(({ theme }) => ({
  maxWidth: "1280px",
  width: "100%",
  marginInline: "auto",
  paddingInline: theme.spacing(2),
  paddingTop: theme.spacing(4),
  paddingBottom: theme.spacing(9),
  flex: "1 1 0%",
  position: "relative",
  display: "flex",
  flexDirection: "column",
  gap: theme.spacing(2),

  [theme.breakpoints.up("sm")]: {
    paddingInline: theme.spacing(3),
    paddingBottom: theme.spacing(5),
    gap: theme.spacing(3),
  },
}));
