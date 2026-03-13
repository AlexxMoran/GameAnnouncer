import { CreateGameForm } from "@pages/games/ul/create-game-form";
import { useDialog } from "@shared/hooks/use-dialog";
import type { IEditGameDto, IGameDto } from "@shared/services/api/games-api-service/types";
import type { TEntityId } from "@shared/types/commonEntity.types";
import { useSnackbar } from "notistack";
import { useCallback } from "react";
import { useTranslation } from "react-i18next";

export const useEditGame = (editGame: (gameId: TEntityId, params: IEditGameDto) => Promise<unknown>) => {
  const { t } = useTranslation();
  const { enqueueSnackbar } = useSnackbar();
  const { openDialog, closeDialog } = useDialog();

  const handleEditGame = useCallback(
    async ({ id }: IGameDto, values: IEditGameDto) => {
      const result = await editGame(id, values);

      if (result) {
        enqueueSnackbar(t("texts.gameEditingSuccess"), { variant: "success" });
        closeDialog();
      }
    },
    [editGame, enqueueSnackbar, closeDialog, t]
  );

  const handleOpenEditDialog = useCallback(
    (game: IGameDto) => {
      openDialog({
        title: t("actions.editGame"),
        children: <CreateGameForm initialValues={game} onSubmit={(values) => handleEditGame(game, values)} />,
      });
    },
    [openDialog, handleEditGame, t]
  );

  return { handleOpenEditDialog };
};
