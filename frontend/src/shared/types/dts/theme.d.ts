import { Theme as MuiTheme } from "@mui/material/styles";

declare module "@emotion/react" {
  export interface Theme extends MuiTheme {}
}

declare module "@mui/material/styles" {
  interface TypeBackground {
    accent: string;
  }
}
