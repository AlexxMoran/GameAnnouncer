import type { AutocompleteProps } from "@mui/material";

export interface IAutocompleteProps<
  TOption,
  TMultiple extends boolean | undefined = false,
  TDisableClearable extends boolean | undefined = false,
  TFreeSolo extends boolean | undefined = false
> extends Omit<
    AutocompleteProps<TOption, TMultiple, TDisableClearable, TFreeSolo>,
    "renderInput"
  > {
  label?: string;
  name?: string;
  error?: boolean;
  helperText?: string;
  required?: boolean;
  onLastItemVisible?: () => Promise<void>;
}
