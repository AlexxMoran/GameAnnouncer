import { EAppRoutes } from "@shared/constants/appRoutes";
import { useRootService } from "@shared/hooks/use-root-service";
import type { ILoginDto } from "@shared/services/api/auth-api-service/types";
import { AuthWindow } from "@widgets/auth-window/ui";
import { observer } from "mobx-react-lite";
import { useSnackbar } from "notistack";
import type { FC } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router";

export const LoginPage: FC = observer(() => {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { authService } = useRootService();
  const { enqueueSnackbar } = useSnackbar();

  const handleLogin = async (params: ILoginDto) => {
    try {
      await authService.login(params);

      navigate(EAppRoutes.Announcements);
      enqueueSnackbar(t("texts.successLogin"), { variant: "success" });
    } catch (_) {
      /* empty */
    }
  };

  return (
    <AuthWindow
      titleText={t("actions.login")}
      buttonText={t("actions.login")}
      haveAccountText={t("texts.haveNoAccount")}
      urlText={t("actions.register")}
      url={EAppRoutes.Registration}
      onSubmit={handleLogin}
    />
  );
});
