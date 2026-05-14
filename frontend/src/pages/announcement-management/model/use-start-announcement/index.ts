import { useDialog } from "@shared/hooks/use-dialog";
import { useSnackbar } from "notistack";
import { useCallback } from "react";
import { useTranslation } from "react-i18next";

export const useStartAnnouncement = (startAnnouncement: () => Promise<unknown>) => {
  const { t } = useTranslation();
  const { enqueueSnackbar } = useSnackbar();
  const { confirm } = useDialog();

  const handleStartAnnouncement = useCallback(async () => {
    const result = await confirm({
      title: t("actions.startTournament"),
      children: t("texts.confirmStartTournament"),
      confirmationText: t("actions.start"),
    });

    if (result) {
      const { closeDialog, setIsLoading } = result;

      setIsLoading(true);
      const response = await startAnnouncement();

      if (response) {
        enqueueSnackbar(t("texts.tournamentStartedMayTheBestWin"), { variant: "success" });
      }

      closeDialog();
    }
  }, [startAnnouncement, confirm, enqueueSnackbar, t]);

  return { handleStartAnnouncement };
};
