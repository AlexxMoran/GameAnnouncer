import { RegistrationRequestForm } from "@pages/announcements/ui/registration-request-form";
import { useDialog } from "@shared/hooks/use-dialog";
import { useRootService } from "@shared/hooks/use-root-service";
import type { IAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import type { ICreateRegistrationRequestDto } from "@shared/services/api/registration-requests-api-service/types";
import { isEmpty } from "lodash";
import { useSnackbar } from "notistack";
import { useCallback } from "react";
import { useTranslation } from "react-i18next";

export const useCreateRegistrationRequest = () => {
  const { t } = useTranslation();
  const { openDialog, closeDialog, confirm } = useDialog();
  const { enqueueSnackbar } = useSnackbar();
  const { registrationRequestsApiService: apiService } = useRootService();

  const createRegistrationRequest = useCallback(
    async (params: ICreateRegistrationRequestDto) => {
      try {
        const response = await apiService.createRegistrationRequest(params);

        if (response) {
          enqueueSnackbar(t("texts.sendRequestSuccess"), { variant: "success" });
          closeDialog();
        }
      } finally {
        /* empty */
      }
    },
    [apiService, enqueueSnackbar, t, closeDialog]
  );

  const handleCreateRegistrationRequest = useCallback(
    async ({ id, registration_form }: IAnnouncementDto) => {
      const { fields } = registration_form || {};

      if (fields && !isEmpty(fields)) {
        openDialog({
          title: t("actions.sendRequest"),
          children: (
            <RegistrationRequestForm
              fieldList={fields}
              onSubmit={(values) =>
                createRegistrationRequest({
                  announcement_id: id,
                  form_responses: Object.entries(values).map(([formFieldId, value]) => ({
                    form_field_id: +formFieldId,
                    value: value.toString(),
                  })),
                })
              }
            />
          ),
        });
      } else {
        const result = await confirm({
          title: t("actions.sendRequest"),
          children: t("texts.sendRequestConfirmation"),
          confirmationText: t("actions.send"),
        });

        if (result) {
          createRegistrationRequest({ announcement_id: id });
        }
      }
    },
    [t, openDialog, confirm, createRegistrationRequest]
  );

  return { handleCreateRegistrationRequest };
};
