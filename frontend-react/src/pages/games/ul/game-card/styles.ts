import { css } from "@emotion/react";
import styled from "@emotion/styled";
import type { IGameImgStyledProps } from "@pages/games/ul/game-card/types";
import { T } from "@shared/ui/typography";

export const GameImgStyled = styled.div<IGameImgStyledProps>`
  width: 100%;
  height: 160px;
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

export const AnnouncementsCountStyled = styled("div")(({ theme }) => ({
  padding: `${theme.spacing(1)} ${theme.spacing(3)}`,
  width: "fit-content",
  position: "absolute",
  top: theme.spacing(2),
  left: theme.spacing(2),
  borderRadius: +theme.shape.borderRadius * 6 + "px",
  backgroundColor: theme.palette.secondary.main,
}));

export const GameCardWrapperStyled = styled("div")(({ theme }) => ({
  position: "relative",
  display: "flex",
  flexDirection: "column",
  gap: 8,
  height: "380px",
  padding: theme.spacing(1),
  backgroundColor: theme.palette.background.paper,
  boxShadow: theme.shadows[8],
  borderRadius: +theme.shape.borderRadius * 6 + "px",
}));

export const GameDescriptionStyled = styled(T)`
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  hyphens: auto;
`;
