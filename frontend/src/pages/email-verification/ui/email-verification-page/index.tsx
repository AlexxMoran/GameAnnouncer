import { EAppRoutes } from "@shared/constants/appRoutes";
import { useRootService } from "@shared/hooks/use-root-service";
import { Spinner } from "@shared/ui/spinner";
import { useSnackbar } from "notistack";
import type { FC } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate, useSearchParams } from "react-router";
import { useAsync } from "react-use";

// TODO обработать кейс если при верификации будет ошибка сервера
export const EmailVerificationPage: FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { authApiService } = useRootService();
  const [searchParams] = useSearchParams();
  const { enqueueSnackbar } = useSnackbar();

  const token = searchParams.get("token");

  const { loading } = useAsync(async () => {
    if (token) {
      try {
        await authApiService.verifyEmail(token);

        enqueueSnackbar(t("texts.emailVerificationSuccess"), {
          variant: "success",
        });
      } finally {
        navigate(EAppRoutes.Login);
      }
    } else {
      enqueueSnackbar(t("texts.emptyVerifyTokenAlert"), { variant: "error" });
    }
  });

  return <>{loading && <Spinner type="backdrop" />}</>;
};
