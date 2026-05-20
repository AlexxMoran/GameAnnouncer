import { createCancellationRequestValidationSchema } from "@pages/announcement-management/model/create-cancellation-request-validation-schema";
import { RequestCancellationFields } from "@pages/announcement-management/ui/request-cancellation-fields";
import type { IRequestCancellationFormProps } from "@pages/announcement-management/ui/request-cancellation-form/types";
import { useDialog } from "@shared/hooks/use-dialog";
import { Form } from "@shared/ui/form";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const RequestCancellationForm: FC<IRequestCancellationFormProps> = (props) => {
  const { onSubmit, request } = props;
  const { closeDialog } = useDialog();
  const { t } = useTranslation();

  const { user } = request;

  const initialValues = {
    cancellation_reason: "",
  };

  const validationSchema = createCancellationRequestValidationSchema(t);

  return (
    <Form
      onSubmit={(values) => onSubmit?.(values)}
      onCancel={closeDialog}
      formikConfig={{ initialValues, validationSchema }}
      fields={() => <RequestCancellationFields nickname={user.nickname} />}
      confirmButtonText={t("actions.reject")}
      isForDialog
    />
  );
};
