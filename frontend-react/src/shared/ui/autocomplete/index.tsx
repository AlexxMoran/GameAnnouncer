import { Autocomplete as MuiAutocomplete } from "@mui/material";
import type { IAutocompleteProps } from "@shared/ui/autocomplete/types";
import { TextField } from "@shared/ui/text-field";
import { useTranslation } from "react-i18next";

export const Autocomplete = <
  TOption,
  TMultiple extends boolean | undefined = false,
  TDisableClearable extends boolean | undefined = false,
  TFreeSolo extends boolean | undefined = false
>(
  props: IAutocompleteProps<TOption, TMultiple, TDisableClearable, TFreeSolo>
) => {
  const { t } = useTranslation();
  const { name, label, required, helperText, error, ...rest } = props;

  return (
    <MuiAutocomplete
      {...rest}
      size="small"
      noOptionsText={t("texts.noOptions")}
      renderInput={(params) => (
        <TextField
          {...params}
          name={name}
          label={label}
          required={required}
          helperText={helperText}
          error={error}
        />
      )}
    />
  );
};
