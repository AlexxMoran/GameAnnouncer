import { Box } from "@shared/ui/box";
import { Spinner } from "@shared/ui/spinner";
import { TextFieldStyled } from "@shared/ui/text-field/styles";
import type { ITextFieldProps } from "@shared/ui/text-field/types";
import { forwardRef } from "react";
import { useTranslation } from "react-i18next";

export const TextField = forwardRef<HTMLInputElement, ITextFieldProps>((props, ref) => {
  const { loading, endAdornment, ...rest } = props;

  const { t } = useTranslation();

  return (
    <TextFieldStyled
      size="small"
      ref={ref}
      placeholder={t("placeholders.enter")}
      variant="outlined"
      {...rest}
      slotProps={{
        ...props.slotProps,
        input: {
          ...props.slotProps?.input,
          endAdornment: (
            <Box display="flex" alignItems="center" gap={2}>
              {loading ? <Spinner color="inherit" size={20} /> : null}
              {endAdornment}
            </Box>
          ),
        },
      }}
    />
  );
});
