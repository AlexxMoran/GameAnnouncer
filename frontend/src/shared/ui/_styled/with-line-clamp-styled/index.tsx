import { css, styled } from "@mui/material";
import type { IWithLineClampStyledProps } from "@shared/ui/_styled/with-line-clamp-styled/types";
import { T } from "@shared/ui/typography";

export const WithLineClampStyled = styled(T)<IWithLineClampStyledProps>`
  word-break: break-all;

  ${({ lineClamp }) =>
    lineClamp &&
    css`
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: ${lineClamp};
      overflow: hidden;
      hyphens: auto;
    `}
`;
