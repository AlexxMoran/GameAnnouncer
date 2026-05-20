import type { ICancellationRequestFields } from "@pages/announcement-management/model/create-cancellation-request-validation-schema/types";
import { RequestCancellationForm } from "@pages/announcement-management/ui/request-cancellation-form";
import { useDialog } from "@shared/hooks/use-dialog";
import { ERegistrationRequestActions } from "@shared/services/api/registration-requests-api-service/constants";
import type {
  IEditRegistrationRequestDto,
  IRegistrationRequestDto,
} from "@shared/services/api/registration-requests-api-service/types";
import { useSnackbar } from "notistack";
import { useCallback } from "react";
import { useTranslation } from "react-i18next";

export const useCancelRequestRequest = (
  request: IRegistrationRequestDto,
  changeRequestStatus: (params: IEditRegistrationRequestDto) => Promise<unknown>
) => {
  const { t } = useTranslation();
  const { enqueueSnackbar } = useSnackbar();
  const { openDialog, closeDialog } = useDialog();

  const handleCancelRequest = useCallback(
    async (values: ICancellationRequestFields) => {
      const result = await changeRequestStatus({ ...values, action: ERegistrationRequestActions.Cancel });

      if (result) {
        enqueueSnackbar(t("texts.applicationCancelledSuccessfully"), { variant: "success" });
        closeDialog();
      }
    },
    [changeRequestStatus, enqueueSnackbar, closeDialog, t]
  );

  const handleOpenRequestCancellationDialog = useCallback(() => {
    openDialog({
      title: t("actions.rejectApplication"),
      children: <RequestCancellationForm onSubmit={handleCancelRequest} request={request} />,
    });
  }, [t, openDialog, handleCancelRequest, request]);

  return { handleOpenRequestCancellationDialog };
};
