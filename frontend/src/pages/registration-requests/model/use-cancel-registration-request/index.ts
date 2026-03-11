import { useDialog } from "@shared/hooks/use-dialog";
import { ERegistrationRequestActions } from "@shared/services/api/registration-requests-api-service/constants";
import type {
  IEditRegistrationRequestDto,
  IRegistrationRequestDto,
} from "@shared/services/api/registration-requests-api-service/types";
import type { TEntityId } from "@shared/types/commonEntity.types";
import { useSnackbar } from "notistack";
import { useCallback } from "react";
import { useTranslation } from "react-i18next";

export const useCancelRegistrationRequest = (
  editEntity: (gameId: TEntityId, params: IEditRegistrationRequestDto) => Promise<unknown>
) => {
  const { t } = useTranslation();
  const { confirm } = useDialog();
  const { enqueueSnackbar } = useSnackbar();

  const handleCancelRequest = useCallback(
    async ({ id }: IRegistrationRequestDto) => {
      const result = await confirm({
        title: t("actions.cancelRequest"),
        children: t("texts.cancelRequestConfirmation"),
        confirmationText: t("actions.cancel"),
      });

      if (result) {
        const { closeDialog, setIsLoading } = result;

        setIsLoading(true);

        const response = await editEntity(id, {
          action: ERegistrationRequestActions.Cancel,
        });

        if (response) {
          enqueueSnackbar(t("texts.cancelRequestSuccess"), {
            variant: "success",
          });
        }

        closeDialog();
      }
    },
    [t, confirm, editEntity, enqueueSnackbar]
  );

  return { handleCancelRequest };
};
