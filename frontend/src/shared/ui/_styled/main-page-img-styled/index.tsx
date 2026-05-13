import { styled } from "@mui/material";
import type { IMainPageImgStyledProps } from "@shared/ui/_styled/main-page-img-styled/types";

export const MainPageImgStyled = styled("div")<IMainPageImgStyledProps>`
  position: relative;
  background-image: url(${({ imgUrl }) => imgUrl});
  background-repeat: no-repeat;
  background-size: cover;
  width: 100%;
  padding-top: min(calc(100% / 1.5), 340px);
  background-position: ${({ backgroundPosition }) => backgroundPosition};

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(180deg, rgba(26, 30, 36, 0.75) 0%, rgba(20, 24, 28, 0.92) 100%);
  }
`;
