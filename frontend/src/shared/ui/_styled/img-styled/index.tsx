import { css } from "@emotion/react";
import { styled } from "@mui/material";
import type { IEntityImgStyledProps } from "@shared/ui/_styled/img-styled/types";

export const ImgStyled = styled("div")<IEntityImgStyledProps>`
  position: relative;

  ${({ imgUrl }) =>
    imgUrl &&
    css`
      background-image: url(${imgUrl});
      background-position: center;
      background-size: cover;
      background-repeat: no-repeat;
    `}
`;
