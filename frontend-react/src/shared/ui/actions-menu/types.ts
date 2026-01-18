import type { TMaybe } from "@shared/types/main.types";
import type { Dispatch, FC, ReactNode, SetStateAction } from "react";

export interface IMenuAction {
  id: number;
  title?: string;
  onClick?: (actionId: number) => void;
  disabled?: boolean;
  hidden?: boolean;
  tooltip?: string;
  icon?: ReactNode;
}

export interface IActionsMenuProps {
  actionList: IMenuAction[];
  children: FC<{
    onClick: () => void;
    ref: Dispatch<SetStateAction<TMaybe<HTMLElement>>>;
  }>;
}
