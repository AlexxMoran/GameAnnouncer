import { styled } from "@mui/material";

export const GamesWrapperStyled = styled("div")(({ theme }) => ({
  display: "grid",
  gap: theme.spacing(8),
  position: "relative",
  gridTemplateColumns: "1fr",

  [theme.breakpoints.up("sm")]: {
    gridTemplateColumns: "repeat(2, 1fr)",
  },

  [theme.breakpoints.up("lg")]: {
    gridTemplateColumns: "repeat(3, 1fr)",
  },
}));
