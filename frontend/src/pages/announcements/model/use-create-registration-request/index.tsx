import { RegistrationRequestConfirmation } from "@pages/announcements/ui/registration-request-confirmation";
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
    async (announcement: IAnnouncementDto) => {
      const { id, registration_form } = announcement;
      const { fields } = registration_form || {};

      if (fields && !isEmpty(fields)) {
        openDialog({
          title: t("actions.takePart"),
          children: (
            <RegistrationRequestForm
              fieldList={fields}
              announcement={announcement}
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
          title: t("actions.takePart"),
          children: <RegistrationRequestConfirmation announcement={announcement} />,
          confirmationText: t("actions.submitApplication"),
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
