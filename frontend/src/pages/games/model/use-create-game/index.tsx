import { CreateGameForm } from "@pages/games/ul/create-game-form";
import { useDialog } from "@shared/hooks/use-dialog";
import type { ICreateGameDto } from "@shared/services/api/games-api-service/types";
import { useSnackbar } from "notistack";
import { useCallback } from "react";
import { useTranslation } from "react-i18next";

export const useCreateGame = (createGame: (params: ICreateGameDto) => Promise<unknown>) => {
  const { t } = useTranslation();
  const { enqueueSnackbar } = useSnackbar();
  const { openDialog, closeDialog } = useDialog();

  const handleCreateGame = useCallback(
    async (values: ICreateGameDto) => {
      const result = await createGame(values);

      if (result) {
        enqueueSnackbar(t("texts.gameAddingSuccess"), { variant: "success" });
        closeDialog();
      }
    },
    [createGame, enqueueSnackbar, closeDialog, t]
  );

  const handleOpenCreateDialog = useCallback(() => {
    openDialog({
      title: t("actions.addGame"),
      children: <CreateGameForm onSubmit={handleCreateGame} />,
    });
  }, [t, openDialog, handleCreateGame]);

  return { handleOpenCreateDialog };
};
