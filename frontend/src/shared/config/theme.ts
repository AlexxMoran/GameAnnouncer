import { createTheme } from "@mui/material";

export const THEME = createTheme({
  spacing: 4,
  palette: {
    mode: "dark",
    background: {
      default: "rgb(19, 19, 20) ",
      paper: "rgb(27, 28, 29)",
    },
  },
  typography: { fontFamily: '"Montserrat", sans-serif' },
  components: {
    MuiDialog: {
      styleOverrides: {
        paper: ({ theme }) => ({
          borderRadius: +theme.shape.borderRadius * 4,
          background: theme.palette.background.paper,
        }),
      },
    },
    MuiMenu: {
      styleOverrides: {
        paper: ({ theme }) => ({
          background: theme.palette.background.paper,
        }),
      },
    },
  },
});
