import { styled } from "@mui/material";

export const CardsWrapperStyled = styled("div")(({ theme }) => ({
  display: "grid",
  gap: theme.spacing(2),
  position: "relative",
  gridTemplateColumns: "1fr",

  [theme.breakpoints.up("md")]: {
    gridTemplateColumns: "repeat(2, 1fr)",
    gap: theme.spacing(3),
  },

  [theme.breakpoints.up("lg")]: {
    gridTemplateColumns: "repeat(3, 1fr)",
    gap: theme.spacing(3),
  },
}));
