import SearchOffIcon from "@mui/icons-material/SearchOff";
import { useIntersectionTrigger } from "@shared/hooks/use-intersection-trigger";
import type { TObjectAny } from "@shared/types/main.types";
import { CardsWrapperStyled } from "@shared/ui/_styled/cards-wrapper-styled";
import { Box } from "@shared/ui/box";
import type {
  IEntityListProps,
  IInfiniteScrollListProps,
  IScrollTriggerProps,
} from "@shared/ui/infinite-scroll-list/types";
import { Spinner } from "@shared/ui/spinner";
import { T } from "@shared/ui/typography";
import { observer } from "mobx-react-lite";
import { Fragment, type FC, type RefObject } from "react";
import { useTranslation } from "react-i18next";

const defaultItemKeyExtractor = <T extends TObjectAny>(item: T) => item.id;

const EntityList = observer(
  <T extends TObjectAny>({
    list,
    containerComponent: Container = CardsWrapperStyled,
    itemKeyExtractor = defaultItemKeyExtractor,
    renderItem,
  }: IEntityListProps<T>) => {
    return (
      <Container>
        {list.map((item) => (
          <Fragment key={itemKeyExtractor(item)}>{renderItem(item)}</Fragment>
        ))}
      </Container>
    );
  }
);

const ScrollTrigger: FC<IScrollTriggerProps> = ({ onTrigger }) => {
  const { ref } = useIntersectionTrigger(onTrigger);

  return <div ref={ref as RefObject<HTMLDivElement>} style={{ height: 1 }} />;
};

export const InfiniteScrollList = observer(<T extends TObjectAny>(props: IInfiniteScrollListProps<T>) => {
  const {
    containerComponent,
    isInitialLoading,
    isPaginating,
    hasMore,
    totalCount,
    list,
    itemKeyExtractor,
    renderItem,
    onLoadMore,
    noDataIcon: NoDataIcon = SearchOffIcon,
    noDataSubtitle,
    noDataTitle,
  } = props;

  const { t } = useTranslation();
  const resolvedNoDataTitle = noDataTitle || t("texts.nothingFound");
  const resolvedNoDataSubtitle = noDataSubtitle || t("texts.tryChangeSearchParameters");

  if (isInitialLoading) {
    return <Spinner type="backdrop" />;
  }

  if (totalCount === 0) {
    return (
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          py: { xs: 6, md: 10 },
          textAlign: "center",
        }}
      >
        <NoDataIcon sx={{ fontSize: 56, color: "text.disabled", mb: 2 }} />
        <T variant="h6" sx={{ color: "text.secondary", mb: 1 }}>
          {resolvedNoDataTitle}
        </T>
        <T variant="body2" sx={{ color: "text.disabled", maxWidth: 360, hyphens: "none" }}>
          {resolvedNoDataSubtitle}
        </T>
      </Box>
    );
  }

  if (list.length === 0 && totalCount !== 0) {
    return (
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          py: { xs: 6, md: 10 },
          textAlign: "center",
        }}
      >
        <SearchOffIcon sx={{ fontSize: 56, color: "text.disabled", mb: 2 }} />
        <T variant="h6" sx={{ color: "text.secondary", mb: 1 }}>
          {t("texts.nothingFound")}
        </T>
        <T variant="body2" sx={{ color: "text.disabled", maxWidth: 360 }}>
          {t("texts.tryChangeSearchParameters")}
        </T>
      </Box>
    );
  }

  return (
    <div>
      <EntityList
        list={list}
        containerComponent={containerComponent}
        itemKeyExtractor={itemKeyExtractor}
        renderItem={renderItem}
      />
      {hasMore && (
        <Fragment>
          <ScrollTrigger onTrigger={onLoadMore} />
          <Box display="flex" justifyContent="center" alignItems="center" width="100%" height="60px">
            {isPaginating && <Spinner size={40} />}
          </Box>
        </Fragment>
      )}
    </div>
  );
});
