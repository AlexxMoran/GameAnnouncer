import type { JSX } from "react";

export interface IBottomBarProps {
  navItemList: {
    label: string;
    icon: JSX.Element;
    url: string;
  }[];
}
