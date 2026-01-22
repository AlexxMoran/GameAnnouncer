import { styled } from "@mui/material";
import type { IWithLineClampStyledProps } from "@shared/ui/_styled/with-line-clamp-styled/types";
import { T } from "@shared/ui/typography";

export const WithLineClampStyled = styled(T)<IWithLineClampStyledProps>`
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: ${({ lineClamp = 1 }) => lineClamp};
  overflow: hidden;
  hyphens: auto;
`;
