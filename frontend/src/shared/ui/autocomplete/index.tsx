import { Autocomplete as MuiAutocomplete } from "@mui/material";
import type { IEntityIdField } from "@shared/types/commonEntity.types";
import { Option } from "@shared/ui/autocomplete/option";
import type { IAutocompleteProps } from "@shared/ui/autocomplete/types";
import { TextField } from "@shared/ui/text-field";
import { useTranslation } from "react-i18next";

export const Autocomplete = <
  TOption extends string | number | IEntityIdField,
  TMultiple extends boolean | undefined = false,
  TDisableClearable extends boolean | undefined = false,
  TFreeSolo extends boolean | undefined = false,
>(
  props: IAutocompleteProps<TOption, TMultiple, TDisableClearable, TFreeSolo>
) => {
  const { name, label, required, helperText, error, onLastItemVisible, loading, ...rest } = props;

  const { t } = useTranslation();

  return (
    <MuiAutocomplete
      {...rest}
      size="small"
      noOptionsText={t("texts.noOptions")}
      slotProps={{ listbox: { sx: { maxHeight: "200px" } } }}
      renderOption={(props, _, counter, ownerState) => {
        const isLastOption = counter.index === rest.options.length - 1;

        return (
          <Option
            onLastItemVisible={onLastItemVisible}
            label={ownerState.getOptionLabel(rest.options[counter.index])}
            isLastOption={isLastOption}
            liAttributes={props}
          />
        );
      }}
      renderInput={(params) => (
        <TextField
          {...params}
          name={name}
          label={label}
          required={required}
          helperText={helperText}
          error={error}
          loading={loading}
          endAdornment={params.InputProps.endAdornment}
          slotProps={{ input: params.InputProps }}
        />
      )}
    />
  );
};
