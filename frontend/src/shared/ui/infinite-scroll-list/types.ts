import type { TMaybe, TObjectAny } from "@shared/types/main.types";
import type { ElementType, ReactNode } from "react";

export interface IEntityListProps<T extends TObjectAny> {
  list: T[];
  renderItem: (item: T) => ReactNode;
  itemKeyExtractor?: (item: T) => string | number;
  containerComponent?: ElementType;
}

export interface IInfiniteScrollListProps<T extends TObjectAny> extends IEntityListProps<T> {
  isInitialLoading: boolean;
  isPaginating: boolean;
  hasMore: boolean;
  total: TMaybe<number>;
  onLoadMore: () => Promise<void>;
}
