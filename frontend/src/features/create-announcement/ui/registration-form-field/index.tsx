import type { IRegistrationFormFieldProps } from "@features/create-announcement/ui/registration-form-field/types";
import { RegistrationFormOption } from "@features/create-announcement/ui/registration-form-option";
import AddIcon from "@mui/icons-material/Add";
import DeleteOutlinedIcon from "@mui/icons-material/DeleteOutlined";
import { FormControlLabel } from "@mui/material";
import { ERegistrationFormFieldTypes } from "@shared/services/api/announcements-api-service/constants";
import { Autocomplete } from "@shared/ui/autocomplete";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { Card } from "@shared/ui/card";
import { Checkbox } from "@shared/ui/checkbox";
import { IconButton } from "@shared/ui/icon-button";
import { TextField } from "@shared/ui/text-field";
import { Tooltip } from "@shared/ui/tooltip";
import { T } from "@shared/ui/typography";
import { memo, type FC } from "react";
import { useTranslation } from "react-i18next";

export const RegistrationFormField: FC<IRegistrationFormFieldProps> = memo((props) => {
  const { t } = useTranslation();

  const {
    fieldKey,
    errors,
    options,
    field_type,
    label,
    required,
    index,
    onChangeOption,
    onDeleteOption,
    onChangeType,
    onChangeLabel,
    onDeleteField,
    onAddOption,
    onChangeCheckbox,
  } = props;

  const fieldErrors = errors?.[fieldKey];
  const optionList = Object.entries(options || {});

  const optionErrors = (() => {
    try {
      if (fieldErrors?.options) {
        return JSON.parse(fieldErrors.options) as Record<string, string>;
      }
    } catch (_) {
      /* empty */
    }
  })();

  return (
    <Card
      sx={{
        display: "flex",
        flexDirection: "column",
        backgroundColor: (theme) => theme.palette.background.accent,
        gap: 1,
        p: 2,
      }}
      key={fieldKey}
    >
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <T variant="caption">
          {t("texts.fieldNumberText")}
          {index + 1}
        </T>
        <Tooltip title={t("actions.deleteField")}>
          <IconButton color="error" sx={{ alignSelf: "center" }} onClick={() => onDeleteField?.(fieldKey)}>
            <DeleteOutlinedIcon />
          </IconButton>
        </Tooltip>
      </Box>
      <Box display="flex" gap={1}>
        <TextField
          value={label}
          label={t("entities.name")}
          sx={{ flex: 1 }}
          onChange={(event) => onChangeLabel?.(event, fieldKey)}
          error={!!fieldErrors?.label}
          helperText={fieldErrors?.label}
          required
        />
        <Autocomplete
          value={field_type}
          label={t("entities.type")}
          options={Object.values(ERegistrationFormFieldTypes)}
          sx={{ flex: 0.5 }}
          onChange={(_, value) => onChangeType?.(value, fieldKey)}
          error={!!fieldErrors?.field_type}
          helperText={fieldErrors?.field_type}
          required
        />
      </Box>
      {field_type === ERegistrationFormFieldTypes.Select && (
        <Box display="flex" flexDirection="column" gap={1}>
          <T variant="caption">{t("texts.optionList")}</T>
          {optionList.map(([optionKey, value], index) => {
            const error = optionErrors?.[optionKey];

            return (
              <RegistrationFormOption
                key={optionKey}
                error={error}
                fieldKey={fieldKey}
                optionValue={value}
                isDeletionDisabled={index === 0 && optionList.length === 1}
                optionKey={optionKey}
                onChangeOption={onChangeOption}
                onDeleteOption={onDeleteOption}
              />
            );
          })}
        </Box>
      )}
      {field_type === ERegistrationFormFieldTypes.Select && (
        <Button
          variant="text"
          startIcon={<AddIcon />}
          sx={{ alignSelf: "start" }}
          onClick={() => onAddOption?.(fieldKey)}
        >
          {t("actions.addOption")}
        </Button>
      )}
      {field_type !== ERegistrationFormFieldTypes.Boolean && (
        <FormControlLabel
          name="withRegistrationForm"
          label={t("texts.requiredField")}
          control={<Checkbox size="small" checked={required} />}
          onChange={(_, checked) => onChangeCheckbox?.(checked, fieldKey)}
        />
      )}
    </Card>
  );
});
