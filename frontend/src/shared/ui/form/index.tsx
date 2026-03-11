import { trimObjectValues } from "@shared/lib/trimObjectValues";
import type { TObjectAny } from "@shared/types/main.types";
import { Box } from "@shared/ui/box";
import { ButtonGroup } from "@shared/ui/button-group";
import { DialogContent } from "@shared/ui/dialog";
import { FormFieldsWrapper } from "@shared/ui/form/form-fields-wrapper";
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
    disableOnSameValues = false,
    onSubmit,
    onValidation,
    onValuesChange,
    onCancel,
    children,
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

  const isSubmitButtonDisabled =
    !formik.isValid || (disableOnSameValues && isEqual(formik.initialValues, formik.values));

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
          <DialogContent>
            <Box display="flex" flexDirection="column" gap={3} mt={0.5}>
              {children}
              <FormFieldsWrapper>
                <Fields />
              </FormFieldsWrapper>
            </Box>
          </DialogContent>
          <ButtonGroup
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
          <FormFieldsWrapper>
            <Fields />
          </FormFieldsWrapper>
          <ButtonGroup
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
