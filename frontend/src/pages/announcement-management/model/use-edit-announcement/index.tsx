import { CreateAnnouncementForm } from "@features/create-announcement/ui/create-announcement-form";
import { useDialog } from "@shared/hooks/use-dialog";
import type { IAnnouncementDto, IEditAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import type { TMaybe } from "@shared/types/main.types";
import { useSnackbar } from "notistack";
import { useCallback } from "react";
import { useTranslation } from "react-i18next";

export const useEditAnnouncement = (
  editAnnouncement: (params: IEditAnnouncementDto) => Promise<unknown>,
  announcement?: TMaybe<IAnnouncementDto>
) => {
  const { t } = useTranslation();
  const { enqueueSnackbar } = useSnackbar();
  const { openDialog, closeDialog } = useDialog();

  const handleEditAnnouncement = useCallback(
    async (values: IEditAnnouncementDto) => {
      const result = await editAnnouncement(values);

      if (result) {
        enqueueSnackbar(t("texts.tournamentEditedSuccessfully"), { variant: "success" });
        closeDialog();
      }
    },
    [editAnnouncement, enqueueSnackbar, closeDialog, t]
  );

  const handleOpenEditDialog = useCallback(() => {
    openDialog({
      title: t("actions.editTournament"),
      children: (
        <CreateAnnouncementForm announcement={announcement} onSubmit={(values) => handleEditAnnouncement(values)} />
      ),
    });
  }, [openDialog, handleEditAnnouncement, t, announcement]);

  return { handleOpenEditDialog };
};
