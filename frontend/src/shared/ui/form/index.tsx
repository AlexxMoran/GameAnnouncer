import { trimObjectValues } from "@shared/lib/trimObjectValues";
import type { TObjectAny } from "@shared/types/main.types";
import { Box } from "@shared/ui/box";
import { DialogContent } from "@shared/ui/dialog";
import { DialogButtonGroup } from "@shared/ui/dialog-button-group";
import type { IFormProps } from "@shared/ui/form/types";
import { FormikContext, useFormik } from "formik";
import isEqual from "lodash/isEqual";
import { observer } from "mobx-react-lite";
import { useEffect, useState } from "react";

export const FormComponent = <TFormValues extends TObjectAny>(props: IFormProps<TFormValues>) => {
  const {
    formikConfig,
    confirmButtonText,
    cancelButtonText,
    fields: Fields,
    isForDialog = false,
    onSubmit,
    onValidation,
    onValuesChange,
    onCancel,
  } = props;

  const { onSubmit: onFormikSubmit, initialValues, ...otherSettings } = formikConfig;

  const [isSubmitted, setIsSubmitted] = useState(false);

  const formik = useFormik<TFormValues>({
    initialValues,
    onSubmit: onFormikSubmit || ((values: TFormValues) => onSubmit?.(trimObjectValues(values))),
    validateOnBlur: false,
    validateOnChange: isSubmitted,
    ...otherSettings,
  });

  const isSubmitButtonDisabled = !formik.isValid || isEqual(initialValues, formik.values);

  const handleSubmit = async () => {
    await formik.submitForm();
    setIsSubmitted(true);
  };

  useEffect(() => {
    onValidation?.(formik.isValid);
  }, [formik.isValid]);

  useEffect(() => {
    onValuesChange?.(formik.values);
  }, [formik.values]);

  return (
    <FormikContext.Provider value={formik}>
      {isForDialog ? (
        <>
          <DialogContent sx={{ minWidth: { sm: "500px" } }}>
            <Box display="flex" flexDirection="column" gap={3} mt={0.5}>
              <Fields />
            </Box>
          </DialogContent>
          <DialogButtonGroup
            onConfirm={handleSubmit}
            onCancel={onCancel}
            isLoading={formik.isSubmitting}
            disabled={isSubmitButtonDisabled}
            cancellationText={cancelButtonText}
            confirmationText={confirmButtonText}
            isForDialog
          />
        </>
      ) : (
        <Box display="flex" flexDirection="column" gap={5} width="100%">
          <Box display="flex" flexDirection="column" gap={3}>
            <Fields />
          </Box>
          <DialogButtonGroup
            onConfirm={handleSubmit}
            onCancel={onCancel}
            isLoading={formik.isSubmitting}
            disabled={isSubmitButtonDisabled}
            cancellationText={cancelButtonText}
            confirmationText={confirmButtonText}
          />
        </Box>
      )}
    </FormikContext.Provider>
  );
};

export const Form = observer(FormComponent);
