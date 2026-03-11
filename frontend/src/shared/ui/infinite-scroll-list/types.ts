import type { SvgIconComponent } from "@mui/icons-material";
import type { TMaybe, TObjectAny } from "@shared/types/main.types";
import type { ElementType, ReactNode } from "react";

export interface IEntityListProps<T extends TObjectAny> {
  list: T[];
  renderItem: (item: T) => ReactNode;
  itemKeyExtractor?: (item: T) => string | number;
  containerComponent?: ElementType;
}

export interface IInfiniteScrollListProps<T extends TObjectAny> extends IEntityListProps<T> {
  noDataTitle: string;
  noDataSubtitle: string;
  noDataIcon: SvgIconComponent;
  isInitialLoading: boolean;
  isPaginating: boolean;
  hasMore: boolean;
  totalCount: TMaybe<number>;
  onLoadMore: () => Promise<void>;
}

export interface IScrollTriggerProps {
  onTrigger: () => Promise<void>;
}
