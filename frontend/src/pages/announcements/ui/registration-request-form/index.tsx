import { createInitialValues } from "@pages/announcements/lib/create-initial-values";
import { validateRegistrationRequestForm } from "@pages/announcements/model/validate-registration-request-form";
import { RegistrationRequestConfirmation } from "@pages/announcements/ui/registration-request-confirmation";
import { RegistrationRequestFields } from "@pages/announcements/ui/registration-request-fields";
import type { IRegistrationRequestFormProps } from "@pages/announcements/ui/registration-request-form/types";
import { useDialog } from "@shared/hooks/use-dialog";
import { Box } from "@shared/ui/box";
import { Form } from "@shared/ui/form";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const RegistrationRequestForm: FC<IRegistrationRequestFormProps> = (props) => {
  const { onSubmit, fieldList, announcement } = props;

  const { t } = useTranslation();
  const { closeDialog } = useDialog();

  const initialValues = createInitialValues(fieldList);
  const validate = (values: Record<string, string | boolean>) => validateRegistrationRequestForm(fieldList, values, t);

  return (
    <>
      <Box paddingInline={3}>
        <RegistrationRequestConfirmation announcement={announcement} withForm />
      </Box>
      <Form
        onSubmit={(values) => onSubmit?.(values)}
        onCancel={closeDialog}
        formikConfig={{ initialValues, validate }}
        fields={() => <RegistrationRequestFields fieldList={fieldList} />}
        confirmButtonText={t("actions.submitApplication")}
        isForDialog
      />
    </>
  );
};
