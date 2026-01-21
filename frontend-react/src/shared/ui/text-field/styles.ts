import styled from "@emotion/styled";
import { TextField } from "@mui/material";

export const TextFieldStyled = styled(TextField)`
  & label {
    display: inline-block;

    &::first-letter {
      text-transform: uppercase;
    }
  }
`;
