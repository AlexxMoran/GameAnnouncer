import { TopBarStyled } from "@app/top-bar/styles";
import type { ITopBarProps } from "@app/top-bar/types";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import LogoutOutlinedIcon from "@mui/icons-material/LogoutOutlined";
import ManageAccountsOutlinedIcon from "@mui/icons-material/ManageAccountsOutlined";
import { Toolbar } from "@mui/material";
import { EAppRoutes } from "@shared/constants/appRoutes";
import { useDeviceType } from "@shared/hooks/use-device-type";
import { useDialog } from "@shared/hooks/use-dialog";
import { useRootService } from "@shared/hooks/use-root-service";
import { ActionsMenu } from "@shared/ui/actions-menu";
import { Box } from "@shared/ui/box";
import { IconButton } from "@shared/ui/icon-button";
import { Link } from "@shared/ui/link";
import { Tooltip } from "@shared/ui/tooltip";
import type { FC } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router";

export const TopBar: FC<ITopBarProps> = ({ navItemList }) => {
  const { isMobile } = useDeviceType();
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { authService } = useRootService();
  const { confirm } = useDialog();

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
    <TopBarStyled position="sticky" elevation={0}>
      <Toolbar
        sx={{
          display: "flex",
          justifyContent: "space-between",
          maxWidth: "1280px",
          width: "100%",
          mx: "auto",
        }}
      >
        <div>LOGO</div>
        {!isMobile && (
          <>
            <Box display="flex" alignItems="center" gap={4}>
              {navItemList.map(({ url, label }) => (
                <Link key={url} to={url} className="capitalize-first">
                  {label}
                </Link>
              ))}
            </Box>
            <Box display="flex" alignItems="center">
              {isAuthenticated ? (
                <ActionsMenu actionList={actionList}>
                  {({ onClick, ref }) => (
                    <Tooltip title={me?.email}>
                      <IconButton onClick={onClick} ref={ref}>
                        <AccountCircleIcon />
                      </IconButton>
                    </Tooltip>
                  )}
                </ActionsMenu>
              ) : (
                <Link to={EAppRoutes.Login}>{t("actions.login")}</Link>
              )}
            </Box>
          </>
        )}
      </Toolbar>
    </TopBarStyled>
  );
};
