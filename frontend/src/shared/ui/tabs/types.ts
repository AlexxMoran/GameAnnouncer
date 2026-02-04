import type { TabsProps } from "@mui/material";
import type { PropsWithChildren } from "react";

export interface ITab {
  label: string;
  value: string | number;
}

export interface ITabsProps extends TabsProps, PropsWithChildren {
  tabList: ITab[];
}
