import type { IRegistrationFormFields } from "@features/create-announcement/model/validate-registration-form-fields/types";
import { RegistrationFormField } from "@features/create-announcement/ui/registration-form-field";
import AddIcon from "@mui/icons-material/Add";
import { ERegistrationFormFieldTypes } from "@shared/services/api/announcements-api-service/constants";
import type { IRegistrationFormField } from "@shared/services/api/announcements-api-service/types";
import type { TMaybe } from "@shared/types/main.types";
import { Button } from "@shared/ui/button";
import { useFormikContext } from "formik";
import isUndefined from "lodash/isUndefined";
import { observer } from "mobx-react-lite";
import { useCallback, useMemo, type ChangeEvent, type FC } from "react";
import { useTranslation } from "react-i18next";
import { v4 as uuidv4 } from "uuid";

export const RegistrationFormFields: FC = observer(() => {
  const { t } = useTranslation();
  const { errors, values, setFieldValue } = useFormikContext<IRegistrationFormFields>();

  const { fields } = values;

  const handleAddField = useCallback(() => {
    setFieldValue("fields", (currentFields: Record<string, IRegistrationFormField> = {}) =>
      Object.assign({}, currentFields, {
        [uuidv4()]: {
          field_type: ERegistrationFormFieldTypes.Text,
          label: "",
          required: false,
        },
      })
    );
  }, [setFieldValue]);

  const handleChangeType = useCallback(
    (value: TMaybe<ERegistrationFormFieldTypes>, key: string) => {
      setFieldValue("fields", (currentFields: Record<string, IRegistrationFormField> = {}) => {
        if (currentFields[key] && value) {
          currentFields[key] = Object.assign(
            {},
            currentFields[key],
            { field_type: value },
            value === ERegistrationFormFieldTypes.Select ? { options: { [uuidv4()]: "" } } : {}
          );
        }

        return currentFields;
      });
    },
    [setFieldValue]
  );

  const handleChangeLabel = useCallback(
    (event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>, key: string) => {
      setFieldValue("fields", (currentFields: Record<string, IRegistrationFormField> = {}) => {
        if (currentFields[key]) {
          currentFields[key] = { ...currentFields[key], label: event.target.value };
        }

        return currentFields;
      });
    },
    [setFieldValue]
  );

  const handleAddOption = useCallback(
    (key: string) => {
      setFieldValue("fields", (currentFields: Record<string, IRegistrationFormField> = {}) => {
        if (currentFields[key]) {
          const options = { ...currentFields[key].options, [uuidv4()]: "" };

          currentFields[key].options = options;
        }

        return currentFields;
      });
    },
    [setFieldValue]
  );

  const handleDeleteField = useCallback(
    (key: string) => {
      setFieldValue("fields", (currentFields: Record<string, IRegistrationFormField> = {}) => {
        if (currentFields[key]) {
          delete currentFields[key];
        }

        return currentFields;
      });
    },
    [setFieldValue]
  );

  const handleDeleteOption = useCallback(
    (fieldKey: string, optionKey: string) => {
      setFieldValue("fields", (currentFields: Record<string, IRegistrationFormField> = {}) => {
        if (currentFields[fieldKey]) {
          const options = { ...currentFields[fieldKey].options };

          if (!isUndefined(options?.[optionKey])) {
            delete options?.[optionKey];

            currentFields[fieldKey].options = options;
          }
        }

        return currentFields;
      });
    },
    [setFieldValue]
  );

  const handleChangeOption = useCallback(
    (event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>, fieldKey: string, optionKey: string) => {
      setFieldValue("fields", (currentFields: Record<string, IRegistrationFormField> = {}) => {
        if (currentFields[fieldKey]) {
          const options = { ...currentFields[fieldKey].options };

          if (!isUndefined(options?.[optionKey])) {
            options[optionKey] = event.target.value;

            currentFields[fieldKey].options = options;
          }
        }

        return currentFields;
      });
    },
    [setFieldValue]
  );

  const handleChangeCheckbox = useCallback(
    (checked: boolean, key: string) => {
      setFieldValue("fields", (currentFields: Record<string, IRegistrationFormField> = {}) => {
        if (currentFields[key]) {
          currentFields[key] = { ...currentFields[key], required: checked };
        }

        return currentFields;
      });
    },
    [setFieldValue]
  );

  const memoErrors = useMemo(() => errors["fields"], [errors]);

  return (
    <>
      {Object.entries(fields || {}).map(([fieldKey, fieldValues]) => (
        <RegistrationFormField
          key={fieldKey}
          errors={memoErrors}
          fieldKey={fieldKey}
          onAddOption={handleAddOption}
          onChangeCheckbox={handleChangeCheckbox}
          onChangeLabel={handleChangeLabel}
          onChangeOption={handleChangeOption}
          onChangeType={handleChangeType}
          onDeleteField={handleDeleteField}
          onDeleteOption={handleDeleteOption}
          {...fieldValues}
        />
      ))}
      <Button variant="text" startIcon={<AddIcon />} sx={{ alignSelf: "start" }} onClick={handleAddField}>
        {t("actions.addField")}
      </Button>
    </>
  );
});
