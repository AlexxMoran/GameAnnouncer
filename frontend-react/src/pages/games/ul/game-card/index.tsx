import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import {
  AnnouncementsCountStyled,
  GameCardWrapperStyled,
  GameDescriptionStyled,
  GameImgStyled,
} from "@pages/games/ul/game-card/styles";
import type { IGameCardProps } from "@pages/games/ul/game-card/types";
import { ActionsMenu } from "@shared/ui/actions-menu";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { IconButton } from "@shared/ui/icon-button";
import { T } from "@shared/ui/typography";
import { forwardRef } from "react";
import { useTranslation } from "react-i18next";

export const GameCard = forwardRef<HTMLDivElement, IGameCardProps>(
  (props, ref) => {
    const { game, actionList } = props;

    const { t } = useTranslation();
    const { image_url, announcements_count, name, description } = game;

    return (
      <GameCardWrapperStyled ref={ref}>
        <GameImgStyled imgUrl={image_url}>
          <AnnouncementsCountStyled>
            {t("countedEntities.announcement", { count: announcements_count })}
          </AnnouncementsCountStyled>
        </GameImgStyled>
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
          <T variant="h6">{name}</T>
          {description && (
            <GameDescriptionStyled variant="body1">
              {description}
            </GameDescriptionStyled>
          )}
          <Button sx={{ mt: "auto" }}>{t("texts.allTournaments")}</Button>
        </Box>
      </GameCardWrapperStyled>
    );
  }
);
