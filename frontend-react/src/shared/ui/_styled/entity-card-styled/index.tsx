import { styled } from "@mui/material";
import { CardStyled } from "@shared/ui/_styled/card-styled";

export const EntityCardStyled = styled(CardStyled)(({ theme }) => ({
  height: "300px",
  gap: theme.spacing(2),
  padding: theme.spacing(1),
  boxShadow: theme.shadows[8],
  transition: "transform 0.3s ease, box-shadow 0.3s ease",
  cursor: "pointer",

  "&:hover": {
    boxShadow: theme.shadows[16],
    transform: "scale(1.03)",
  },
}));
