import { Box } from "@shared/ui/box";
import type { IBoxProps } from "@shared/ui/box/types";
import type { FC, PropsWithChildren } from "react";

export const FormFieldsWrapper: FC<PropsWithChildren<IBoxProps>> = ({ children, ...otherProps }) => {
  return (
    <Box display="flex" flexDirection="column" {...otherProps} gap={2.5}>
      {children}
    </Box>
  );
};
