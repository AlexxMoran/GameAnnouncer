import type { IAuthFields } from "@features/auth/model/create-validation-schema/types";
import { RegistrationConfirmation } from "@pages/registration/ui/registration-confirmation";
import { EAppRoutes } from "@shared/constants/appRoutes";
import { useDialog } from "@shared/hooks/use-dialog";
import { useRootService } from "@shared/hooks/use-root-service";
import { AuthWindow } from "@widgets/auth-window/ui";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const RegistrationPage: FC = () => {
  const { t } = useTranslation();
  const { authApiService } = useRootService();
  const { openDialog } = useDialog();

  const handleRegister = async (values: IAuthFields) => {
    try {
      await authApiService.register({
        password: values.password,
        email: values.username,
      });

      openDialog({
        title: t("texts.welcome"),
        children: <RegistrationConfirmation email={values.username} />,
        maxWidth: "xs",
      });
    } finally {
      /* empty */
    }
  };

  return (
    <AuthWindow
      titleText={t("entities.registration")}
      buttonText={t("actions.register")}
      haveAccountText={t("texts.haveAccount")}
      urlText={t("actions.login")}
      url={EAppRoutes.Login}
      onSubmit={handleRegister}
    />
  );
};
