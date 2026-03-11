import { useDialog } from "@shared/hooks/use-dialog";
import type { IGameDto } from "@shared/services/api/games-api-service/types";
import { useSnackbar } from "notistack";
import { useCallback } from "react";
import { useTranslation } from "react-i18next";

export const useDeleteGame = (deleteGame: (gameId: number) => Promise<unknown>) => {
  const { t } = useTranslation();
  const { enqueueSnackbar } = useSnackbar();
  const { confirm } = useDialog();

  const handleDeleteGame = useCallback(
    async ({ id }: IGameDto) => {
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
    },
    [deleteGame, confirm, enqueueSnackbar, t]
  );

  return { handleDeleteGame };
};
