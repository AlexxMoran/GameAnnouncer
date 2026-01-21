import { styled } from "@mui/material";
import type { IWithLineClampStyledProps } from "@shared/styles/with-line-clamp-styled/types";
import { T } from "@shared/ui/typography";

export const WithLineClampStyled = styled(T)<IWithLineClampStyledProps>`
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: ${({ lineClamp = 3 }) => lineClamp};
  overflow: hidden;
  hyphens: auto;
`;
