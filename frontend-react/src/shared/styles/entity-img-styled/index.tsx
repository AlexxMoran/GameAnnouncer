import { css } from "@emotion/react";
import { styled } from "@mui/material";

import type { IEntityImgStyledProps } from "@shared/styles/entity-img-styled/types";

export const EntityImgStyled = styled("div")<IEntityImgStyledProps>`
  width: 100%;
  height: 140px;
  border-radius: ${({ theme }) => +theme.shape.borderRadius * 6}px;
  position: relative;

  ${({ imgUrl, theme }) =>
    imgUrl
      ? css`
          background-image: url(${imgUrl});
          background-position: center;
          background-size: cover;
          background-repeat: no-repeat;
        `
      : css`
          border: 1px solid ${theme.palette.divider};
        `}
`;
