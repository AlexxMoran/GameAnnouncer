import type { JSX } from "react";

export interface ITopBarProps {
  navItemList: {
    label: string;
    icon: JSX.Element;
    url: string;
  }[];
}
