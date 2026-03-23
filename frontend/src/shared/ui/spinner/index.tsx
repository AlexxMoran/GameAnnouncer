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
    <Box width="100%" height="100%" display="flex" justifyContent="center" alignItems="center">
      <CircularProgress {...rest} size={80} />
    </Box>
  );
};
