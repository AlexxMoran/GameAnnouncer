import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import type { IGameCardProps } from "@pages/games/ul/game-card/types";
import { ImgStyled } from "@shared/ui/_styled/img-styled";
import { WithLineClampStyled } from "@shared/ui/_styled/with-line-clamp-styled";
import { ActionsMenu } from "@shared/ui/actions-menu";
import { Box } from "@shared/ui/box";
import { Card } from "@shared/ui/card";
import { Chip } from "@shared/ui/chip";
import { IconButton } from "@shared/ui/icon-button";
import { type FC } from "react";
import { useTranslation } from "react-i18next";

export const GameCard: FC<IGameCardProps> = (props) => {
  const { game, actionList } = props;

  const { t } = useTranslation();
  const { image_url, announcements_count, name, description } = game;

  return (
    <Card sx={{ height: "375px" }}>
      <ImgStyled imgUrl={image_url} sx={{ height: "50%" }}>
        <Chip
          label={t("countedEntities.announcement", { count: announcements_count })}
          sx={{
            position: "absolute",
            backgroundColor: (theme) => theme.palette.secondary.main,
            top: (theme) => theme.spacing(1.5),
            left: (theme) => theme.spacing(1.5),
            color: (theme) => theme.palette.getContrastText(theme.palette.secondary.main),
          }}
        />
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
      </ImgStyled>
      <Box display="flex" flexDirection="column" gap={0.5} flex={1} pb={3} pt={1.5} px={1.5}>
        <WithLineClampStyled lineClamp={1} variant="h6">
          {name}
        </WithLineClampStyled>
        {description && (
          <WithLineClampStyled lineClamp={5} variant="body2" color="textSecondary">
            {description}
          </WithLineClampStyled>
        )}
      </Box>
    </Card>
  );
};
