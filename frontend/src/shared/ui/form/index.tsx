import { trimObjectValues } from "@shared/helpers/trimObjectValues";
import type { TObjectAny } from "@shared/types/main.types";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import type { IFormProps } from "@shared/ui/form/types";
import { FormikContext, useFormik } from "formik";
import { observer } from "mobx-react-lite";
import { useEffect, useState } from "react";

export const FormComponent = <TFormValues extends TObjectAny>(props: IFormProps<TFormValues>) => {
  const {
    formikConfig,
    buttonText,
    fields: Fields,
    wrapperStyles,
    cancelButton,
    onSubmit,
    onValidation,
    onValuesChange,
  } = props;

  const { onSubmit: onFormikSubmit, ...otherSettings } = formikConfig;

  const [isSubmitted, setIsSubmitted] = useState(false);

  const formik = useFormik<TFormValues>({
    onSubmit: onFormikSubmit || ((values: TFormValues) => onSubmit?.(trimObjectValues(values))),
    validateOnBlur: false,
    validateOnChange: isSubmitted,
    ...otherSettings,
  });

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
      <Box display="flex" flexDirection="column" gap={10} width="100%" {...wrapperStyles}>
        <Box display="flex" flexDirection="column" gap={6}>
          <Fields />
        </Box>
        {cancelButton ? (
          <Box display="flex" gap={2} alignSelf="flex-end">
            <Button variant="outlined" onClick={cancelButton.onCancel}>
              {cancelButton.text}
            </Button>
            <Button onClick={handleSubmit} loading={formik.isSubmitting} disabled={!formik.isValid}>
              {buttonText}
            </Button>
          </Box>
        ) : (
          <Button onClick={handleSubmit} loading={formik.isSubmitting} disabled={!formik.isValid}>
            {buttonText}
          </Button>
        )}
      </Box>
    </FormikContext.Provider>
  );
};

export const Form = observer(FormComponent);
