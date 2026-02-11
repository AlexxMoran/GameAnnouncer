import { Switch as MuiSwitch } from "@mui/material";
import type { ISwitchProps } from "@shared/ui/switch/types";
import type { FC } from "react";

export const Switch: FC<ISwitchProps> = (props) => {
  return <MuiSwitch {...props} />;
};
