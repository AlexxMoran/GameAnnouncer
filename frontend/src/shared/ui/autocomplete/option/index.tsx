import { ListItem } from "@mui/material";
import { useIntersectionTrigger } from "@shared/hooks/use-intersection-trigger";
import type { IOptionProps } from "@shared/ui/autocomplete/option/types";
import { type FC, type RefObject } from "react";

export const Option: FC<IOptionProps> = ({ onLastItemVisible, label, isLastOption, liAttributes }) => {
  const { ref } = useIntersectionTrigger(onLastItemVisible);

  return (
    <ListItem ref={isLastOption ? (ref as RefObject<HTMLLIElement>) : null} {...liAttributes}>
      {label}
    </ListItem>
  );
};
