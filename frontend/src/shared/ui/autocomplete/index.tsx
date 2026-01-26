import { ListItem, Autocomplete as MuiAutocomplete } from "@mui/material";
import type { IEntityIdField } from "@shared/types/commonEntity.types";
import type { IAutocompleteProps } from "@shared/ui/autocomplete/types";
import { ElementObserver } from "@shared/ui/element-observer";
import { TextField } from "@shared/ui/text-field";
import { type RefObject } from "react";
import { useTranslation } from "react-i18next";

export const Autocomplete = <
  TOption extends string | number | IEntityIdField,
  TMultiple extends boolean | undefined = false,
  TDisableClearable extends boolean | undefined = false,
  TFreeSolo extends boolean | undefined = false,
>(
  props: IAutocompleteProps<TOption, TMultiple, TDisableClearable, TFreeSolo>,
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
      renderOption={(
        { key: _, ...otherProps },
        option,
        counter,
        ownerState,
      ) => {
        const isLastOption = counter.index === rest.options.length - 1;
        const label = ownerState.getOptionLabel?.(option);
        const optionId = typeof option === "object" ? option.id : label;

        const key =
          typeof option === "object" ? optionId : (option as string | number);

        return isLastOption ? (
          <ElementObserver onVisible={onLastItemVisible} key={key}>
            {({ ref }) => (
              <ListItem ref={ref as RefObject<HTMLLIElement>} {...otherProps}>
                {label}
              </ListItem>
            )}
          </ElementObserver>
        ) : (
          <ListItem key={key} {...otherProps}>
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
