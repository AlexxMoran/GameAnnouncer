import { HeaderStyled, LayoutStyled } from "@app/layout/styles";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import LogoutOutlinedIcon from "@mui/icons-material/LogoutOutlined";
import ManageAccountsOutlinedIcon from "@mui/icons-material/ManageAccountsOutlined";
import { useScrollTrigger } from "@mui/material";
import { EAppRoutes } from "@shared/constants/appRoutes";
import { useDialog } from "@shared/hooks/use-dialog";
import { useRootService } from "@shared/hooks/use-root-service";
import { ActionsMenu } from "@shared/ui/actions-menu";
import { Box } from "@shared/ui/box";
import { Fab } from "@shared/ui/fab-button";
import { IconButton } from "@shared/ui/icon-button";
import { Link } from "@shared/ui/link";
import { Tooltip } from "@shared/ui/tooltip";
import { Zoom } from "@shared/ui/zoom";
import type { FC, PropsWithChildren } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router";

export const Layout: FC<PropsWithChildren> = ({ children }) => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { authService } = useRootService();
  const { confirm } = useDialog();

  const trigger = useScrollTrigger({
    disableHysteresis: true,
    threshold: 500,
  });

  const { isAuthenticated, me, logout } = authService;

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

  const handleNavigateToSettings = () => {
    navigate(EAppRoutes.AccountSettings);
  };

  const handleScrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const actionList = [
    {
      id: 1,
      title: t("texts.accountSettings"),
      onClick: handleNavigateToSettings,
      icon: <ManageAccountsOutlinedIcon />,
    },
    {
      id: 2,
      title: t("actions.logout"),
      onClick: handleLogout,
      icon: <LogoutOutlinedIcon />,
    },
  ];

  return (
    <Box display="flex" flexDirection="column" height="100vh">
      <HeaderStyled>
        <div>LOGO</div>
        <Box display="flex" alignItems="center" gap={4}>
          {!isAuthenticated && (
            <Link to={EAppRoutes.Login}>{t("actions.login")}</Link>
          )}
          <Link to={EAppRoutes.Games}>{t("pageTitles.games")}</Link>
          <Link to={EAppRoutes.Announcements}>
            {t("pageTitles.announcements")}
          </Link>
          <Link to={EAppRoutes.MyAnnouncements}>
            {t("texts.myAnnouncementsTitle")}
          </Link>
        </Box>
        <Box display="flex" alignItems="center">
          {isAuthenticated && (
            <ActionsMenu actionList={actionList}>
              {({ onClick, ref }) => (
                <Tooltip title={me?.email}>
                  <IconButton onClick={onClick} ref={ref}>
                    <AccountCircleIcon />
                  </IconButton>
                </Tooltip>
              )}
            </ActionsMenu>
          )}
        </Box>
      </HeaderStyled>
      <LayoutStyled>{children}</LayoutStyled>
      <Zoom in={trigger}>
        <Fab
          onClick={handleScrollToTop}
          sx={{
            position: "fixed",
            bottom: 32,
            right: 32,
          }}
          size="medium"
          aria-label="scroll back to top"
        >
          <KeyboardArrowUpIcon />
        </Fab>
      </Zoom>
    </Box>
  );
};
