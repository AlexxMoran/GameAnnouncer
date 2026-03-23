import { EAppRoutes } from "@shared/constants/appRoutes";
import { useDialog } from "@shared/hooks/use-dialog";
import { useRootService } from "@shared/hooks/use-root-service";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router";

export const useLogout = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { authService } = useRootService();
  const { confirm } = useDialog();

  const { logout } = authService;

  const handleLogout = async () => {
    const result = await confirm({
      title: t("entities.confirmation"),
      children: t("texts.logoutConfirmation"),
    });

    if (result) {
      const { setIsLoading, closeDialog } = result;

      setIsLoading(true);

      await logout();

      navigate(EAppRoutes.Login);
      closeDialog();
    }
  };

  return { handleLogout };
};
