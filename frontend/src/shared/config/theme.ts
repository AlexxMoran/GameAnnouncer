import { createTheme } from "@mui/material";

export const THEME = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: "#4fc3f7",
      light: "#8bf6ff",
      dark: "#0093c4",
      contrastText: "#0a0c0f",
    },
    secondary: {
      main: "#ffb74d",
      light: "#ffe97d",
      dark: "#c88719",
      contrastText: "#0a0c0f",
    },
    background: {
      default: "#1a1e24",
      paper: "#14181c",
      accent: "#1b2026",
    },
    text: {
      primary: "#e8eaed",
      secondary: "#9aa0a6",
      disabled: "#5f6368",
    },
    divider: "rgba(232, 234, 237, 0.12)",
    error: {
      main: "#f44336",
    },
    warning: {
      main: "#ffb74d",
    },
    success: {
      main: "#66bb6a",
    },
    info: {
      main: "#4fc3f7",
    },
    action: {
      hover: "#19262E",
      selected: "#1D333F",
      disabled: "#54575B",
      disabledBackground: "#2D3135;",
    },
  },
  typography: {
    fontFamily: '"Montserrat", sans-serif',
    h1: {
      fontSize: "2.5rem", // 40px
      fontWeight: 700,
      lineHeight: 1.2,
      "@media (min-width:600px)": {
        fontSize: "3rem", // 48px
      },
      "@media (min-width:900px)": {
        fontSize: "4rem", // 64px
      },
      "@media (min-width:1200px)": {
        fontSize: "5rem", // 80px
      },
      "@media (min-width:1536px)": {
        fontSize: "6rem", // 96px
      },
    },
    h2: {
      fontSize: "2rem", // 32px
      fontWeight: 600,
      lineHeight: 1.3,
      "@media (min-width:600px)": {
        fontSize: "2.5rem", // 40px
      },
      "@media (min-width:900px)": {
        fontSize: "3rem", // 48px
      },
      "@media (min-width:1200px)": {
        fontSize: "3.5rem", // 56px
      },
      "@media (min-width:1536px)": {
        fontSize: "3.75rem", // 60px
      },
    },
    h3: {
      fontSize: "1.75rem", // 28px
      fontWeight: 600,
      lineHeight: 1.4,
      "@media (min-width:600px)": {
        fontSize: "2rem", // 32px
      },
      "@media (min-width:900px)": {
        fontSize: "2.25rem", // 36px
      },
      "@media (min-width:1200px)": {
        fontSize: "2.5rem", // 40px
      },
      "@media (min-width:1536px)": {
        fontSize: "3rem", // 48px
      },
    },
    h4: {
      fontSize: "1.5rem", // 24px
      fontWeight: 600,
      lineHeight: 1.4,
      "@media (min-width:600px)": {
        fontSize: "1.75rem", // 28px
      },
      "@media (min-width:900px)": {
        fontSize: "2rem", // 32px
      },
      "@media (min-width:1200px)": {
        fontSize: "2.125rem", // 34px
      },
      "@media (min-width:1536px)": {
        fontSize: "2.125rem", // 34px
      },
    },
    h5: {
      fontSize: "1.25rem", // 20px
      fontWeight: 600,
      lineHeight: 1.5,
      "@media (min-width:600px)": {
        fontSize: "1.35rem", // 22px
      },
      "@media (min-width:900px)": {
        fontSize: "1.5rem", // 24px
      },
    },
    h6: {
      fontSize: "1.125rem", // 18px
      fontWeight: 600,
      lineHeight: 1.5,
      "@media (min-width:600px)": {
        fontSize: "1.2rem", // 19px
      },
      "@media (min-width:900px)": {
        fontSize: "1.25rem", // 20px
      },
    },
    subtitle1: {
      fontSize: "1rem", // 16px
      fontWeight: 400,
      lineHeight: 1.5,
      "@media (min-width:900px)": {
        fontSize: "1.1rem", // 17.6px
      },
    },
    subtitle2: {
      fontSize: "0.875rem", // 14px
      fontWeight: 500,
      lineHeight: 1.5,
      "@media (min-width:600px)": {
        fontSize: "0.9rem", // 14.4px
      },
      "@media (min-width:900px)": {
        fontSize: "0.875rem",
      },
    },
    body1: {
      fontSize: "1rem", // 16px
      fontWeight: 400,
      lineHeight: 1.5,
      "@media (min-width:900px)": {
        fontSize: "1.05rem", // 16.8px
      },
      "@media (min-width:1200px)": {
        fontSize: "1.1rem", // 17.6px
      },
    },
    body2: {
      fontSize: "0.875rem", // 14px
      fontWeight: 400,
      lineHeight: 1.5,
      "@media (min-width:600px)": {
        fontSize: "0.9rem", // 14.4px
      },
    },
    button: {
      fontSize: "0.875rem", // 14px (единый размер)
      fontWeight: 500,
      lineHeight: 1.75,
      textTransform: "uppercase",
    },
    caption: {
      fontSize: "0.7rem", // 11.2px
      fontWeight: 400,
      lineHeight: 1.66,
      "@media (min-width:600px)": {
        fontSize: "0.75rem", // 12px
      },
    },
    overline: {
      fontSize: "0.7rem", // 11.2px
      fontWeight: 400,
      lineHeight: 2.66,
      textTransform: "uppercase",
      "@media (min-width:600px)": {
        fontSize: "0.75rem", // 12px
      },
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        "#root": {
          height: "100vh",
        },
      },
    },
    MuiDialog: {
      styleOverrides: {
        paper: ({ theme }) => ({
          background: theme.palette.background.paper,
          borderRadius: 0,
          "@media (min-width:600px)": {
            borderRadius: +theme.shape.borderRadius * 4,
          },
        }),
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: ({ theme }) => ({
          backgroundImage: "none",
          borderColor: theme.palette.divider,
          borderWidth: 1,
          borderStyle: "solid",
        }),
      },
    },
    MuiCard: {
      styleOverrides: {
        root: ({ theme }) => ({
          display: "flex",
          flexDirection: "column",
          backgroundColor: theme.palette.background.paper,
          border: "1px solid",
          borderColor: theme.palette.divider,
          borderRadius: 10,
          textDecoration: "none",
        }),
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: "none",
        },
      },
    },
    MuiOutlinedInput: {
      styleOverrides: {
        root: ({ theme }) => ({
          backgroundColor: "#22262C",
          borderRadius: 20,
          "& fieldset": {
            borderColor: theme.palette.divider,
          },
          "&:hover fieldset": {
            borderColor: theme.palette.primary.dark,
          },
          "&.Mui-focused fieldset": {
            borderWidth: 1,
          },
        }),
      },
    },
    MuiBottomNavigationAction: {
      styleOverrides: {
        root: ({ theme }) => ({
          color: theme.palette.text.disabled,
          minWidth: 0,
          padding: "6px 0",
          gap: 0.5,
          transition: "color 0.2s ease",
          "&.Mui-selected": {
            color: theme.palette.primary.main,
          },
        }),
        label: {
          fontSize: "0.65rem",
          fontWeight: 500,
          textTransform: "capitalize",
          "&.Mui-selected": {
            fontSize: "0.65rem",
            fontWeight: 600,
          },
        },
      },
    },
    MuiLinearProgress: {
      variants: [
        {
          props: { color: "success" },
          style: {
            "& .MuiLinearProgress-bar": {
              background: "linear-gradient(90deg, #66bb6a, #4fc3f7)",
            },
          },
        },
        {
          props: { color: "warning" },
          style: {
            "& .MuiLinearProgress-bar": {
              background: "linear-gradient(90deg, #4fc3f7, #ffb74d)",
            },
          },
        },
        {
          props: { color: "error" },
          style: {
            "& .MuiLinearProgress-bar": {
              background: "linear-gradient(90deg, #ffb74d, #f44336)",
            },
          },
        },
      ],
      styleOverrides: {
        root: ({ theme }) => ({
          height: 6,
          borderRadius: 3,
          backgroundColor: theme.palette.action.disabledBackground,
        }),
        bar: {
          borderRadius: 3,
        },
      },
    },
    MuiTabs: {
      styleOverrides: {
        root: ({ theme }) => ({
          borderWidth: 1,
          borderColor: theme.palette.divider,
          borderBottomStyle: "solid",
        }),
        indicator: ({ theme }) => ({
          backgroundColor: theme.palette.primary.main,
          height: 2,
        }),
      },
    },
    MuiTab: {
      styleOverrides: {
        root: {
          "@media (min-width:600px)": {
            fontSize: "0.85rem",
          },
          "&.Mui-selected": {
            fontWeight: 600,
          },
        },
      },
    },
    MuiLink: {
      styleOverrides: {
        root: { "&::first-letter": { textTransform: "capitalize" } },
      },
    },
    MuiStepLabel: {
      styleOverrides: {
        label: {
          "@media (max-width:600px)": {
            fontSize: "0.75rem",
          },
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        root: {
          hyphens: "auto",
          wordBreak: "break-word",
        },
      },
    },
  },
});
