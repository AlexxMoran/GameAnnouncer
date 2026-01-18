import { TextFieldStyled } from "@shared/ui/text-field/styles";
import type { ITextFieldProps } from "@shared/ui/text-field/types";
import { forwardRef } from "react";
import { useTranslation } from "react-i18next";

export const TextField = forwardRef<HTMLInputElement, ITextFieldProps>(
  (props, ref) => {
    const { t } = useTranslation();

    return (
      <TextFieldStyled
        size="small"
        {...props}
        ref={ref}
        placeholder={t("placeholders.enter")}
        variant="outlined"
      />
    );
  }
);
