import { CircularProgress } from "@mui/material";
import { Box } from "@shared/ui/box";
import type { ISpinnerProps } from "@shared/ui/spinner/types";
import { type FC } from "react";

export const Spinner: FC<ISpinnerProps> = (props) => {
  const { type = "single", ...rest } = props;

  if (type === "single") {
    return <CircularProgress {...rest} />;
  }

  return (
    <Box
      width="100%"
      height={type === "backdrop" ? "100%" : "60px"}
      display="flex"
      justifyContent="center"
      alignItems="center"
    >
      <CircularProgress {...rest} size={type === "backdrop" ? 80 : 40} />
    </Box>
  );
};
