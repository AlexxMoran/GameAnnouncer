import { styled } from "@mui/material";

export const CardsWrapperStyled = styled("div")(({ theme }) => ({
  display: "grid",
  gap: theme.spacing(4),
  position: "relative",
  gridTemplateColumns: "1fr",

  [theme.breakpoints.up("sm")]: {
    gridTemplateColumns: "repeat(2, 1fr)",
  },

  [theme.breakpoints.up("md")]: {
    gridTemplateColumns: "repeat(3, 1fr)",
  },

  [theme.breakpoints.up("lg")]: {
    gridTemplateColumns: "repeat(4, 1fr)",
  },
}));
