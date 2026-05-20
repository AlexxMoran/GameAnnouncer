import { useDialog } from "@shared/hooks/use-dialog";
import { ERegistrationRequestActions } from "@shared/services/api/registration-requests-api-service/constants";
import type {
  IEditRegistrationRequestDto,
  IRegistrationRequestDto,
} from "@shared/services/api/registration-requests-api-service/types";
import { useSnackbar } from "notistack";
import { useCallback } from "react";
import { useTranslation } from "react-i18next";

export const useApproveRequest = (
  request: IRegistrationRequestDto,
  changeRequestStatus: (params: IEditRegistrationRequestDto) => Promise<unknown>
) => {
  const { t } = useTranslation();
  const { enqueueSnackbar } = useSnackbar();
  const { confirm } = useDialog();

  const { nickname } = request.user;

  const handleApproveRequest = useCallback(async () => {
    const result = await confirm({
      title: t("actions.acceptApplication"),
      children: t("texts.acceptApplicationIrreversibleConfirm", { nickname }),
      confirmationText: t("actions.accept"),
    });

    if (result) {
      const { closeDialog, setIsLoading } = result;

      setIsLoading(true);
      const response = await changeRequestStatus({ action: ERegistrationRequestActions.Approve });

      if (response) {
        enqueueSnackbar(t("texts.applicationAcceptedSuccessfully"), { variant: "success" });
      }

      closeDialog();
    }
  }, [changeRequestStatus, confirm, enqueueSnackbar, t, nickname]);

  return { handleApproveRequest };
};
