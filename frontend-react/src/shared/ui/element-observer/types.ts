import type { PropsWithChildren } from "react";

export interface IElementObserverProps extends PropsWithChildren {
  onVisible?: () => Promise<void>;
}
