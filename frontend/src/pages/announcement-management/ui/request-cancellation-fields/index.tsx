import type { ICancellationRequestFields } from "@pages/announcement-management/model/create-cancellation-request-validation-schema/types";
import type { IRequestCancellationFieldsProps } from "@pages/announcement-management/ui/request-cancellation-fields/types";
import { TextField } from "@shared/ui/text-field";
import { T } from "@shared/ui/typography";
import { useFormikContext } from "formik";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const RequestCancellationFields: FC<IRequestCancellationFieldsProps> = ({ nickname }) => {
  const { t } = useTranslation();
  const { errors, values, handleChange } = useFormikContext<ICancellationRequestFields>();

  return (
    <>
      <T>{t("texts.rejectApplicationIrreversibleConfirm", { nickname })}</T>
      <TextField
        name="cancellation_reason"
        label={t("texts.rejectionReason")}
        onChange={handleChange}
        value={values["cancellation_reason"]}
        error={!!errors["cancellation_reason"]}
        helperText={errors["cancellation_reason"]}
        rows={4}
        multiline
      />
    </>
  );
};
