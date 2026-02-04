import { styled } from "@mui/material";

export const CardStyled = styled("div")(({ theme }) => ({
  position: "relative",
  display: "flex",
  flexDirection: "column",
  backgroundColor: theme.palette.background.paper,
  borderRadius: +theme.shape.borderRadius * 4 + "px",
}));
