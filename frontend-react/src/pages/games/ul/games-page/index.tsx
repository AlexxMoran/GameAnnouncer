import AddIcon from "@mui/icons-material/Add";
import AddAPhotoOutlinedIcon from "@mui/icons-material/AddAPhotoOutlined";
import DeleteOutlinedIcon from "@mui/icons-material/DeleteOutlined";
import EditOutlinedIcon from "@mui/icons-material/EditOutlined";
import { useTheme } from "@mui/material";
import { GamesService } from "@pages/games/model/games-service";
import { CreateGameForm } from "@pages/games/ul/create-game-form";
import { GameCard } from "@pages/games/ul/game-card";
import { GamesWrapperStyled } from "@pages/games/ul/games-page/styles";
import { ImageUploadForm } from "@pages/games/ul/image-upload-form";
import { useAbortController } from "@shared/hooks/use-abort-controller";
import { useDialog } from "@shared/hooks/use-dialog";
import { useRootService } from "@shared/hooks/use-root-service";
import type {
  ICreateGameDto,
  IEditGameDto,
  IGameDto,
} from "@shared/services/api/games-api-service/types";
import type { IMenuAction } from "@shared/ui/actions-menu/types";
import { Badge } from "@shared/ui/badge";
import { Box } from "@shared/ui/box";
import { ElementObserver } from "@shared/ui/element-observer";
import { Fab } from "@shared/ui/fab-button";
import { Spinner } from "@shared/ui/spinner";
import { T } from "@shared/ui/typography";
import { observer } from "mobx-react-lite";
import { useState, type FC } from "react";
import { useTranslation } from "react-i18next";

export const GamesPage: FC = observer(() => {
  const theme = useTheme();
  const { t } = useTranslation();
  const { gamesApiService } = useRootService();
  const { openDialog, closeDialog, confirm } = useDialog();
  const [gamesService] = useState(() => new GamesService(gamesApiService));
  useAbortController();

  const {
    paginationService,
    createGame,
    deleteGame,
    editGame,
    uploadGameImage,
  } = gamesService;
  const { list, paginate, isInitialLoading, isPaginating, total } =
    paginationService;

  const handleCreateGame = async (values: ICreateGameDto) => {
    const result = await createGame(values);

    if (result) {
      closeDialog();
    }
  };

  const handleEditGame = async ({ id }: IGameDto, values: IEditGameDto) => {
    const result = await editGame(id, values);

    if (result) {
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
        closeDialog();
      }
    }
  };

  const handleUploadImage = async ({ id }: IGameDto, file: File) => {
    const result = await uploadGameImage(id, file);

    if (result) {
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
      children: (
        <CreateGameForm
          initialValues={game}
          onSubmit={(values) => handleEditGame(game, values)}
        />
      ),
    });
  };

  const handleOpenUploadImageDialog = (game: IGameDto) => {
    openDialog({
      title: t("actions.uploadImage"),
      children: (
        <ImageUploadForm
          onUploadImage={(file) => handleUploadImage(game, file)}
        />
      ),
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

  if (isInitialLoading) {
    return <Spinner type="backdrop" />;
  }

  return (
    <Box display="flex" flexDirection="column" gap={8}>
      <Badge badgeContent={total} color="secondary">
        <T variant="h4">{t("pageTitles.games")}</T>
      </Badge>
      {total === 0 && <T variant="body1">{t("texts.haveNoData")}</T>}
      <GamesWrapperStyled>
        {list.map((game, index) =>
          index === list.length - 1 ? (
            <ElementObserver key={game.id} onVisible={paginate}>
              <GameCard game={game} actionList={createGameActionList(game)} />
            </ElementObserver>
          ) : (
            <GameCard
              key={game.id}
              game={game}
              actionList={createGameActionList(game)}
            />
          )
        )}
      </GamesWrapperStyled>
      {isPaginating && <Spinner type="pagination" />}
      <Fab
        onClick={handleOpenCreateDialog}
        tooltip={t("actions.addGame")}
        sx={{
          position: "fixed",
          bottom: theme.spacing(6),
          right: theme.spacing(6),
        }}
      >
        <AddIcon />
      </Fab>
    </Box>
  );
});
