import { css } from "@emotion/react";
import { styled, Typography } from "@mui/material";
import type { ITStylesProps } from "@shared/ui/typography/types";

export const TStyled = styled(Typography)<ITStylesProps>`
  ${({ capitalizeFirst }) =>
    capitalizeFirst &&
    css`
      &::first-letter {
        text-transform: capitalize;
      }
    `}
`;
