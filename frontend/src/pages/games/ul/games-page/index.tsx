import AddIcon from "@mui/icons-material/Add";
import AddAPhotoOutlinedIcon from "@mui/icons-material/AddAPhotoOutlined";
import DeleteOutlinedIcon from "@mui/icons-material/DeleteOutlined";
import EditOutlinedIcon from "@mui/icons-material/EditOutlined";
import { GamesService } from "@pages/games/model/games-service";
import { CreateGameForm } from "@pages/games/ul/create-game-form";
import { GameCard } from "@pages/games/ul/game-card";
import { ImageUploadForm } from "@pages/games/ul/image-upload-form";
import { useDialog } from "@shared/hooks/use-dialog";
import { useRootService } from "@shared/hooks/use-root-service";
import type { ICreateGameDto, IEditGameDto, IGameDto } from "@shared/services/api/games-api-service/types";
import { CardsWrapperStyled } from "@shared/ui/_styled/cards-wrapper-styled";
import type { IMenuAction } from "@shared/ui/actions-menu/types";
import { Badge } from "@shared/ui/badge";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { ElementObserver } from "@shared/ui/element-observer";
import { Spinner } from "@shared/ui/spinner";
import { T } from "@shared/ui/typography";
import { observer } from "mobx-react-lite";
import { useSnackbar } from "notistack";
import { useState, type FC, type RefObject } from "react";
import { useTranslation } from "react-i18next";

export const GamesPage: FC = observer(() => {
  const { t } = useTranslation();
  const { gamesApiService } = useRootService();
  const { enqueueSnackbar } = useSnackbar();
  const { openDialog, closeDialog, confirm } = useDialog();
  const [gamesService] = useState(() => new GamesService(gamesApiService));

  const {
    listData,
    createEntity: createGame,
    deleteEntity: deleteGame,
    editEntity: editGame,
    uploadGameImage,
    paginate,
  } = gamesService;

  const { list, isInitialLoading, isPaginating, total } = listData;

  const handleCreateGame = async (values: ICreateGameDto) => {
    const result = await createGame(values);

    if (result) {
      enqueueSnackbar(t("texts.gameAddingSuccess"), { variant: "success" });
      closeDialog();
    }
  };

  const handleEditGame = async ({ id }: IGameDto, values: IEditGameDto) => {
    const result = await editGame(id, values);

    if (result) {
      enqueueSnackbar(t("texts.gameEditingSuccess"), { variant: "success" });
      closeDialog();
    }
  };

  const handleDeleteGame = async ({ id }: IGameDto) => {
    const result = await confirm({
      title: t("actions.deleteGame"),
      children: t("texts.deletionGameConfirmation"),
      confirmationText: t("actions.delete"),
    });

    if (result) {
      const { closeDialog, setIsLoading } = result;

      setIsLoading(true);
      const response = await deleteGame(id);

      if (response) {
        enqueueSnackbar(t("texts.gameDeletingSuccess"), { variant: "success" });
      }

      closeDialog();
    }
  };

  const handleUploadImage = async ({ id }: IGameDto, file: File) => {
    const result = await uploadGameImage(id, file);

    if (result) {
      enqueueSnackbar(t("texts.gameUploadSuccess"), { variant: "success" });
      closeDialog();
    }
  };

  const handleOpenCreateDialog = () => {
    openDialog({
      title: t("actions.addGame"),
      children: <CreateGameForm onSubmit={handleCreateGame} />,
    });
  };

  const handleOpenEditDialog = (game: IGameDto) => {
    openDialog({
      title: t("actions.editGame"),
      children: <CreateGameForm initialValues={game} onSubmit={(values) => handleEditGame(game, values)} />,
    });
  };

  const handleOpenUploadImageDialog = (game: IGameDto) => {
    openDialog({
      title: t("actions.uploadImage"),
      children: <ImageUploadForm onUploadImage={(file) => handleUploadImage(game, file)} />,
      maxWidth: "sm",
    });
  };

  const createGameActionList = (game: IGameDto): IMenuAction[] => [
    {
      id: 1,
      title: t("actions.uploadImage"),
      onClick: () => handleOpenUploadImageDialog(game),
      icon: <AddAPhotoOutlinedIcon />,
    },
    {
      id: 2,
      title: t("actions.edit"),
      onClick: () => handleOpenEditDialog(game),
      icon: <EditOutlinedIcon />,
    },
    {
      id: 3,
      title: t("actions.delete"),
      onClick: () => handleDeleteGame(game),
      icon: <DeleteOutlinedIcon />,
    },
  ];

  // TODO оптимизировать показ лоадера при пагинации
  return (
    <Box display="flex" flexDirection="column" gap={8} height="100%">
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Badge badgeContent={total} color="secondary">
          <T variant="h4">{t("pageTitles.games")}</T>
        </Badge>
        <Button variant="text" onClick={handleOpenCreateDialog} startIcon={<AddIcon />}>
          {t("actions.addGame")}
        </Button>
      </Box>
      {isInitialLoading && <Spinner type="backdrop" />}
      {total === 0 && <T variant="body1">{t("texts.haveNoData")}</T>}
      {!!list.length && (
        <CardsWrapperStyled>
          {list.map((game, index) =>
            index === list.length - 1 ? (
              <ElementObserver key={game.id} onVisible={paginate}>
                {({ ref }) => (
                  <GameCard
                    ref={ref as RefObject<HTMLDivElement>}
                    game={game}
                    actionList={createGameActionList(game)}
                  />
                )}
              </ElementObserver>
            ) : (
              <GameCard key={game.id} game={game} actionList={createGameActionList(game)} />
            )
          )}
        </CardsWrapperStyled>
      )}
      {isPaginating && <Spinner type="pagination" />}
    </Box>
  );
});
