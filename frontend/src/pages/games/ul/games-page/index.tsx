import AddIcon from "@mui/icons-material/Add";
import { createGameActionList } from "@pages/games/model/create-game-action-list";
import { GamesService } from "@pages/games/model/games-service";
import { useCreateGame } from "@pages/games/model/use-create-game";
import { useDeleteGame } from "@pages/games/model/use-delete-game";
import { useEditGame } from "@pages/games/model/use-edit-game";
import { useUploadGameImage } from "@pages/games/model/use-upload-game-image";
import { GameCard } from "@pages/games/ul/game-card";
import { useRootService } from "@shared/hooks/use-root-service";
import type { IGameDto } from "@shared/services/api/games-api-service/types";
import { PageContentWrapperStyled } from "@shared/ui/_styled/page-content-wrapper-styled";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { InfiniteScrollList } from "@shared/ui/infinite-scroll-list";
import { PageTitle } from "@shared/ui/page-title";
import { observer } from "mobx-react-lite";
import { useCallback, useState, type FC } from "react";
import { useTranslation } from "react-i18next";

export const GamesPage: FC = observer(() => {
  const { t } = useTranslation();
  const { gamesApiService } = useRootService();
  const [gamesService] = useState(() => new GamesService(gamesApiService));

  const {
    listData,
    createEntity: createGame,
    deleteEntity: deleteGame,
    editEntity: editGame,
    uploadGameImage,
    paginate,
  } = gamesService;

  const { handleOpenCreateDialog } = useCreateGame(createGame);
  const { handleDeleteGame } = useDeleteGame(deleteGame);
  const { handleOpenEditDialog } = useEditGame(editGame);
  const { handleOpenUploadImageDialog } = useUploadGameImage(uploadGameImage);

  const renderItem = useCallback(
    (game: IGameDto) => {
      const gameActionList = createGameActionList({
        t,
        game,
        handleDeleteGame,
        handleOpenEditDialog,
        handleOpenUploadImageDialog,
      });

      return <GameCard key={game.id} game={game} actionList={gameActionList} />;
    },
    [t, handleDeleteGame, handleOpenEditDialog, handleOpenUploadImageDialog, createGameActionList]
  );

  return (
    <PageContentWrapperStyled>
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <PageTitle title={t("entities.game.many")} count={listData.filteredCount} />
        <Button variant="text" onClick={handleOpenCreateDialog} startIcon={<AddIcon />}>
          {t("actions.addGame")}
        </Button>
      </Box>
      <InfiniteScrollList renderItem={renderItem} onLoadMore={paginate} {...listData} />
    </PageContentWrapperStyled>
  );
});
