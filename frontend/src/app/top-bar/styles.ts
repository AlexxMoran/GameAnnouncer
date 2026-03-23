import { AppBar, styled } from "@mui/material";

export const TopBarStyled = styled(AppBar)(({ theme }) => ({
  backdropFilter: "blur(12px)",
  backgroundColor: "rgba(20, 24, 28, 0.8)",
  border: "none",
  borderBottom: `1px solid ${theme.palette.divider}`,
}));
