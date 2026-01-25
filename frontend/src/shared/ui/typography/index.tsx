import { TStyled } from "@shared/ui/typography/styles";
import type { ITypographyProps } from "@shared/ui/typography/types";
import { forwardRef } from "react";

export const T = forwardRef<HTMLParagraphElement, ITypographyProps>(
  (props, ref) => <TStyled {...props} ref={ref} />
);
