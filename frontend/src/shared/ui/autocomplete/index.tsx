import { ListItem, Autocomplete as MuiAutocomplete } from "@mui/material";
import type { IAutocompleteProps } from "@shared/ui/autocomplete/types";
import { ElementObserver } from "@shared/ui/element-observer";
import { TextField } from "@shared/ui/text-field";
import type { RefObject } from "react";
import { useTranslation } from "react-i18next";

export const Autocomplete = <
  TOption,
  TMultiple extends boolean | undefined = false,
  TDisableClearable extends boolean | undefined = false,
  TFreeSolo extends boolean | undefined = false
>(
  props: IAutocompleteProps<TOption, TMultiple, TDisableClearable, TFreeSolo>
) => {
  const {
    name,
    label,
    required,
    helperText,
    error,
    onLastItemVisible,
    loading,
    ...rest
  } = props;

  const { t } = useTranslation();

  return (
    <MuiAutocomplete
      {...rest}
      size="small"
      noOptionsText={t("texts.noOptions")}
      slotProps={{ listbox: { sx: { maxHeight: "200px" } } }}
      renderOption={(props, option, counter, ownerState) => {
        // TODO сделать правильный ключ (например id)
        const isLastOption = counter.index === rest.options.length - 1;
        const label = ownerState.getOptionLabel?.(option);

        const optionId =
          typeof option === "object" && option !== null && "id" in option
            ? (option.id as number)
            : label;

        const key = typeof option === "string" ? option : optionId;

        return isLastOption ? (
          <ElementObserver onVisible={onLastItemVisible} key={key}>
            {({ ref }) => (
              <ListItem
                {...props}
                key={key}
                ref={ref as RefObject<HTMLLIElement>}
              >
                {label}
              </ListItem>
            )}
          </ElementObserver>
        ) : (
          <ListItem {...props} key={key}>
            {label}
          </ListItem>
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
