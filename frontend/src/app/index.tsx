import { Layout } from "@app/layout";
import { Pages } from "@app/routes";
import CloseIcon from "@mui/icons-material/Close";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { ruRU } from "@mui/x-date-pickers/locales";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import i18nextInstance from "@shared/config/i18n/config";
import { THEME } from "@shared/config/theme";
import { EAppRoutes } from "@shared/constants/appRoutes";
import { useDeviceType } from "@shared/hooks/use-device-type";
import { RootServiceContext } from "@shared/hooks/use-root-service";
import { DialogProvider } from "@shared/providers/dialog-provider";
import { RootService } from "@shared/services/root-service";
import { Button } from "@shared/ui/button";
import { Spinner } from "@shared/ui/spinner";
import { closeSnackbar, enqueueSnackbar, SnackbarProvider } from "notistack";
import { useState, type FC } from "react";
import { I18nextProvider } from "react-i18next";
import { useNavigate } from "react-router";
import { useAsync } from "react-use";

import "@app/styles/fonts.scss";
import "@app/styles/utils.scss";

const action = (snackbarId: string | number) => (
  <Button
    sx={{ textTransform: "none", color: (theme) => theme.palette.common.white }}
    variant="text"
    onClick={() => closeSnackbar(snackbarId)}
    startIcon={<CloseIcon />}
  >
    {i18nextInstance.t("actions.close")}
  </Button>
);

export const App: FC = () => {
  const navigate = useNavigate();
  const { isMobile } = useDeviceType();

  const [rootService] = useState(
    () =>
      new RootService({
        alertError: (message) => enqueueSnackbar(message, { variant: "error" }),
        redirectToLoginPage: () => navigate(EAppRoutes.Login),
      })
  );

  const { authService } = rootService;

  const { loading } = useAsync(async () => {
    try {
      await authService.refreshToken();
    } catch (_) {
      /* empty */
    }
  });

  // TODO добавить ErrorBoundary
  // TODO вынести в общие стили элементы карточек и стили их позиционаирования
  return (
    <SnackbarProvider
      autoHideDuration={3000}
      action={action}
      maxSnack={3}
      anchorOrigin={{ vertical: isMobile ? "top" : "bottom", horizontal: isMobile ? "center" : "right" }}
    >
      <ThemeProvider theme={THEME}>
        <LocalizationProvider
          dateAdapter={AdapterDayjs}
          adapterLocale="ru"
          localeText={ruRU.components.MuiLocalizationProvider.defaultProps.localeText}
        >
          <I18nextProvider i18n={i18nextInstance}>
            <RootServiceContext.Provider value={rootService}>
              <DialogProvider>
                <CssBaseline />
                {loading ? (
                  <Spinner type="backdrop" />
                ) : (
                  <Layout>
                    <Pages />
                  </Layout>
                )}
              </DialogProvider>
            </RootServiceContext.Provider>
          </I18nextProvider>
        </LocalizationProvider>
      </ThemeProvider>
    </SnackbarProvider>
  );
};
