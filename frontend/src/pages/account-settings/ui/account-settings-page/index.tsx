import { useLogout } from "@features/logout/model/use-logout";
import { AvatarSettings } from "@pages/account-settings/ui/avatar-settings";
import { UserInfoSettings } from "@pages/account-settings/ui/user-info-settings";
import { useDeviceType } from "@shared/hooks/use-device-type";
import { PageContentWrapperStyled } from "@shared/ui/_styled/page-content-wrapper-styled";
import { Button } from "@shared/ui/button";
import { PageTitle } from "@shared/ui/page-title";
import { observer } from "mobx-react-lite";
import { type FC } from "react";
import { useTranslation } from "react-i18next";

export const AccountSettingsPage: FC = observer(() => {
  const { t } = useTranslation();
  const { handleLogout } = useLogout();
  const { isMobile } = useDeviceType();

  return (
    <PageContentWrapperStyled>
      <PageTitle title={t("texts.accountSettings")} />
      <AvatarSettings />
      <UserInfoSettings />
      {isMobile && (
        <Button variant="outlined" color="error" onClick={handleLogout} sx={{ mt: "auto" }}>
          {t("actions.logout")}
        </Button>
      )}
    </PageContentWrapperStyled>
  );
});
