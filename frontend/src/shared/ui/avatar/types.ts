import type { SvgIconTypeMap } from "@mui/material";
import type { OverridableComponent } from "@mui/material/OverridableComponent";
import type { TMaybe } from "@shared/types/main.types";

export interface IAvatarProps {
  username?: string;
  size?: number;
  color?: TMaybe<string>;
  isLoading?: boolean;
  icon?: TMaybe<
    OverridableComponent<SvgIconTypeMap<{}, "svg">> & {
      muiName: string;
    }
  >;
}
