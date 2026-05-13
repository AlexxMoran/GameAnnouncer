import { useDialog } from "@shared/hooks/use-dialog";
import { useSnackbar } from "notistack";
import { useCallback } from "react";
import { useTranslation } from "react-i18next";

export const useCancelAnnouncement = (cancelAnnouncement: () => Promise<unknown>) => {
  const { t } = useTranslation();
  const { enqueueSnackbar } = useSnackbar();
  const { confirm } = useDialog();

  const handleCancelAnnouncement = useCallback(async () => {
    const result = await confirm({
      title: t("actions.cancelAnnouncement"),
      children: t("texts.cancelTournamentIrreversibleConfirm"),
      confirmationColor: "error",
    });

    if (result) {
      const { closeDialog, setIsLoading } = result;

      setIsLoading(true);
      const response = await cancelAnnouncement();

      if (response) {
        enqueueSnackbar(t("texts.tournamentCancelledSuccessfully"), { variant: "success" });
      }

      closeDialog();
    }
  }, [cancelAnnouncement, confirm, enqueueSnackbar, t]);

  return { handleCancelAnnouncement };
};
