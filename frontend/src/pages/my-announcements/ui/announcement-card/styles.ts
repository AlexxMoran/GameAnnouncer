import { styled } from "@mui/material";
import { CardStyled } from "@shared/ui/_styled/card-styled";

export const AnnouncementCardStyled = styled(CardStyled)(({ theme }) => ({
  padding: theme.spacing(1),
  boxShadow: theme.shadows[8],
  // height: "250px",
  flexDirection: "row",
}));
