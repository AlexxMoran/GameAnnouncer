import { Dialog, styled } from "@mui/material";

export const DialogStyled = styled(Dialog)`
  & .MuiDialog-paper {
    border-radius: ${({ theme }) => +theme.shape.borderRadius * 4}px;
  }
`;
