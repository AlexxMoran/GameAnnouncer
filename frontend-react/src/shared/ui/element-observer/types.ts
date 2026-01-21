import type { TMaybe } from "@shared/types/main.types";
import type { FC, RefObject } from "react";

export interface IElementObserverProps {
  onVisible?: () => Promise<void>;
  children: FC<{ ref: RefObject<TMaybe<HTMLElement>> }>;
}
