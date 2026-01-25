import { Button as MuiButton, useTheme } from "@mui/material";
import type { IButtonProps } from "@shared/ui/button/types";
import { type FC } from "react";

export const Button: FC<IButtonProps> = (props) => {
  const theme = useTheme();

  return (
    <MuiButton
      variant="contained"
      size="small"
      {...props}
      sx={{
        textTransform: "none",
        borderRadius: +theme.shape.borderRadius,
        ...props.sx,
      }}
    />
  );
};
