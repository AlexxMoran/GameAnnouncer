import { styled, Tab, Tabs } from "@mui/material";

export const TabStyled = styled(Tab)(({ theme }) => ({
  transition: "all 0.3s ease",
  backgroundColor: "transparent",

  "&.Mui-selected": {
    backgroundColor: theme.palette.background.paper,
  },

  "&:hover": {
    backgroundColor: theme.palette.action.hover,
  },

  "&.Mui-focusVisible": {
    backgroundColor: theme.palette.action.focus,
  },

  "& span.MuiTabs-indicator": {
    display: "none",
  },
}));

export const TabsStyled = styled(Tabs)(() => ({
  "& .MuiTabs-indicator": {
    display: "none",
  },
}));
