import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import type { IGameCardProps } from "@pages/games/ul/game-card/types";
import { CardLabelStyled } from "@shared/ui/_styled/card-label-styled";
import { EntityCardStyled } from "@shared/ui/_styled/entity-card-styled";
import { EntityImgStyled } from "@shared/ui/_styled/entity-img-styled";
import { WithLineClampStyled } from "@shared/ui/_styled/with-line-clamp-styled";
import { ActionsMenu } from "@shared/ui/actions-menu";
import { Box } from "@shared/ui/box";
import { IconButton } from "@shared/ui/icon-button";
import { forwardRef } from "react";
import { useTranslation } from "react-i18next";

export const GameCard = forwardRef<HTMLDivElement, IGameCardProps>(
  (props, ref) => {
    const { game, actionList } = props;

    const { t } = useTranslation();
    const { image_url, announcements_count, name, description } = game;

    return (
      <EntityCardStyled ref={ref}>
        <EntityImgStyled imgUrl={image_url}>
          <CardLabelStyled
            sx={{
              backgroundColor: (theme) => theme.palette.secondary.main,
              top: (theme) => theme.spacing(2),
              left: (theme) => theme.spacing(2),
            }}
          >
            {t("countedEntities.announcement", { count: announcements_count })}
          </CardLabelStyled>
        </EntityImgStyled>
        {actionList?.length && (
          <Box position="absolute" top={8} right={8}>
            <ActionsMenu actionList={actionList}>
              {({ onClick, ref }) => (
                <IconButton ref={ref} onClick={onClick}>
                  <MoreHorizIcon />
                </IconButton>
              )}
            </ActionsMenu>
          </Box>
        )}
        <Box display="flex" flexDirection="column" gap={2} flex={1} p={3}>
          <WithLineClampStyled variant="subtitle2">{name}</WithLineClampStyled>
          {description && (
            <WithLineClampStyled lineClamp={4} variant="caption">
              {description}
            </WithLineClampStyled>
          )}
        </Box>
      </EntityCardStyled>
    );
  }
);
