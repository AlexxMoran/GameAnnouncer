import { EAppRoutes } from "@shared/constants/appRoutes";
import { useRootService } from "@shared/hooks/use-root-service";
import { useSnackbar } from "notistack";
import { useEffect, type ComponentType, type FC, type PropsWithChildren } from "react";
import { useTranslation } from "react-i18next";
import { Navigate } from "react-router";

function withAuth<P extends object>(WrappedComponent: ComponentType<P>): FC<PropsWithChildren<P>> {
  const ProtectedComponent: FC<P> = (props) => {
    const { authService } = useRootService();
    const { enqueueSnackbar } = useSnackbar();
    const { t } = useTranslation();

    const isAuth = authService.isAuthenticated;

    useEffect(() => {
      if (!isAuth) {
        enqueueSnackbar(t("texts.pleaseLogin"), { variant: "warning" });
      }
    }, [isAuth]);

    if (!isAuth) {
      return <Navigate to={EAppRoutes.Login} replace />;
    }

    return <WrappedComponent {...props} />;
  };

  return ProtectedComponent;
}

export default withAuth;
