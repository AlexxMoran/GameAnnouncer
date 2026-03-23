import type { HTMLAttributes } from "react";

export interface IOptionProps {
  liAttributes: HTMLAttributes<HTMLLIElement>;
  onLastItemVisible?: () => Promise<void>;
  label: string;
  isLastOption: boolean;
}
