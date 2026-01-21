import { css } from "@emotion/react";
import { Dialog, DialogTitle, styled } from "@mui/material";
import type { ITStylesProps } from "@shared/ui/dialog/types";

export const DialogTitleStyled = styled(DialogTitle)<ITStylesProps>`
  ${({ capitalizeFirst }) =>
    capitalizeFirst &&
    css`
      &::first-letter {
        text-transform: capitalize;
      }
    `}
`;

export const DialogStyled = styled(Dialog)`
  & .MuiDialog-paper {
    border-radius: ${({ theme }) => +theme.shape.borderRadius * 4}px;
  }
`;
