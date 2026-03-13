import { Box } from "@shared/ui/box";
import { Spinner } from "@shared/ui/spinner";
import { TextFieldStyled } from "@shared/ui/text-field/styles";
import type { ITextFieldProps } from "@shared/ui/text-field/types";
import { forwardRef } from "react";
import { useTranslation } from "react-i18next";

export const TextField = forwardRef<HTMLInputElement, ITextFieldProps>((props, ref) => {
  const { loading, endAdornment, slotProps, ...rest } = props;

  const { t } = useTranslation();

  // TODO сделать так, чтобы компонент был управляемым (чистил по кнопке и тд)
  return (
    <TextFieldStyled
      size="small"
      ref={ref}
      placeholder={t("placeholders.enter")}
      variant="outlined"
      {...rest}
      slotProps={{
        ...slotProps,
        input: {
          ...props.slotProps?.input,
          endAdornment: (endAdornment || loading) && (
            <Box display="flex" alignItems="center" gap={0.5}>
              {loading ? <Spinner color="inherit" size={20} /> : null}
              {endAdornment}
            </Box>
          ),
        },
      }}
    />
  );
});
