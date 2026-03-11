import { styled } from "@mui/material";
import { Box } from "@shared/ui/box";

export const BottomBarStyled = styled(Box)(({ theme }) => ({
  backdropFilter: "blur(12px)",
  backgroundColor: "rgba(20, 24, 28, 0.8)",
  borderTop: `1px solid ${theme.palette.divider}`,
  zIndex: theme.zIndex.appBar,
  position: "fixed",
  bottom: 0,
  left: 0,
  right: 0,
}));
