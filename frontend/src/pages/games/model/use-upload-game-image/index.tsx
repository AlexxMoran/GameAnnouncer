import { ImageUploadForm } from "@pages/games/ul/image-upload-form";
import { useDialog } from "@shared/hooks/use-dialog";
import type { IGameDto } from "@shared/services/api/games-api-service/types";
import { useSnackbar } from "notistack";
import { useCallback } from "react";
import { useTranslation } from "react-i18next";

export const useUploadGameImage = (uploadGameImage: (id: number, image: File) => Promise<unknown>) => {
  const { t } = useTranslation();
  const { enqueueSnackbar } = useSnackbar();
  const { openDialog, closeDialog } = useDialog();

  const handleUploadImage = useCallback(
    async ({ id }: IGameDto, file: File) => {
      const result = await uploadGameImage(id, file);

      if (result) {
        enqueueSnackbar(t("texts.gameUploadSuccess"), { variant: "success" });
        closeDialog();
      }
    },
    [uploadGameImage, enqueueSnackbar, closeDialog, t]
  );

  const handleOpenUploadImageDialog = useCallback(
    (game: IGameDto) => {
      openDialog({
        title: t("actions.uploadImage"),
        children: <ImageUploadForm onUploadImage={(file) => handleUploadImage(game, file)} />,
        maxWidth: "sm",
      });
    },
    [openDialog, handleUploadImage, t]
  );

  return { handleOpenUploadImageDialog };
};
