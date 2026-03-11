import type { TMaybe, TObjectAny } from "@shared/types/main.types";
import type { ElementType, ReactNode } from "react";

export interface IInfiniteScrollListProps<T extends TObjectAny> {
  list: T[];
  renderItem: (item: T) => ReactNode;
  isInitialLoading: boolean;
  isPaginating: boolean;
  total: TMaybe<number>;
  onLoadMore: () => Promise<void>;
  itemKeyExtractor?: (item: T) => string | number;
  containerComponent?: ElementType;
}
