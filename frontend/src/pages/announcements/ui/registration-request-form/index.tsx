import { createInitialValues } from "@pages/announcements/lib/create-initial-values";
import { validateRegistrationRequestForm } from "@pages/announcements/model/validate-registration-request-form";
import { RegistrationRequestFields } from "@pages/announcements/ui/registration-request-fields";
import type { IRegistrationRequestFormProps } from "@pages/announcements/ui/registration-request-form/types";
import { Box } from "@shared/ui/box";
import { Form } from "@shared/ui/form";
import { T } from "@shared/ui/typography";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const RegistrationRequestForm: FC<IRegistrationRequestFormProps> = (props) => {
  const { onSubmit, fieldList } = props;

  const { t } = useTranslation();

  const initialValues = createInitialValues(fieldList);
  const validate = (values: Record<string, string | boolean>) => validateRegistrationRequestForm(fieldList, values, t);

  return (
    <Box display="flex" flexDirection="column" gap={4}>
      <T variant="subtitle2">{t("texts.fillTheFieldsToParticipate")}</T>
      <Form
        onSubmit={(values) => onSubmit?.(values)}
        formikConfig={{ initialValues, validate }}
        fields={() => <RegistrationRequestFields fieldList={fieldList} />}
        buttonText={t("actions.send")}
        wrapperStyles={{ minWidth: "400px" }}
      />
    </Box>
  );
};
