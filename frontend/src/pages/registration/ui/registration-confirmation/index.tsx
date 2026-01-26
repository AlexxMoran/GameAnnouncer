import type { IRegistrationConfirmationProps } from "@pages/registration/ui/registration-confirmation/types";
import { useDialog } from "@shared/hooks/use-dialog";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { T } from "@shared/ui/typography";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const RegistrationConfirmation: FC<IRegistrationConfirmationProps> = ({ email }) => {
  const { t } = useTranslation();
  const { closeDialog } = useDialog();

  return (
    <Box display="flex" flexDirection="column" gap={8}>
      <T>{t("texts.registrationConfirmation", { email })}</T>
      <Button onClick={closeDialog}>{t("texts.ok")}</Button>
    </Box>
  );
};
