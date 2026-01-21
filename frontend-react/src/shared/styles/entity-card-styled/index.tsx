import { styled } from "@mui/material";

export const EntityCardStyled = styled("div")(({ theme }) => ({
  height: "300px",
  position: "relative",
  display: "flex",
  flexDirection: "column",
  gap: theme.spacing(2),
  padding: theme.spacing(1),
  backgroundColor: theme.palette.background.paper,
  boxShadow: theme.shadows[8],
  borderRadius: +theme.shape.borderRadius * 6 + "px",
  transition: "transform 0.3s ease, box-shadow 0.3s ease",
  cursor: "pointer",

  "&:hover": {
    boxShadow: theme.shadows[16],
    transform: "scale(1.03)",
  },
}));
