import { useLogout } from "@features/logout/model/use-logout";
import { createValidationSchema } from "@pages/account-settings/model/create-validation-schema";
import { EditingTextField } from "@pages/account-settings/ui/editing-text-field";
import { useDeviceType } from "@shared/hooks/use-device-type";
import { useRootService } from "@shared/hooks/use-root-service";
import type { IEditUserDto } from "@shared/services/api/auth-api-service/types";
import { PageContentWrapperStyled } from "@shared/ui/_styled/page-content-wrapper-styled";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { Card } from "@shared/ui/card";
import { FormFieldsWrapper } from "@shared/ui/form/form-fields-wrapper";
import { PageTitle } from "@shared/ui/page-title";
import { T } from "@shared/ui/typography";
import { observer } from "mobx-react-lite";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const AccountSettingsPage: FC = observer(() => {
  const { t } = useTranslation();
  const { authApiService, authService } = useRootService();
  const { handleLogout } = useLogout();
  const { isMobile } = useDeviceType();

  const { me, setMe } = authService;

  const handleEditMe = async (values: IEditUserDto) => {
    const { data } = await authApiService.editMe(values);

    setMe(data.data);
  };

  const getValidationSchema = (name: keyof IEditUserDto) => {
    return createValidationSchema(name, t);
  };

  return (
    <PageContentWrapperStyled>
      <PageTitle title={t("texts.accountSettings")} />
      <Card sx={{ p: { xs: 2, lg: 3 } }}>
        <Box display="flex" flexDirection="column" gap={3} width={{ xs: "100%", md: "50%" }}>
          <T variant="h6">{t("texts.usersData")}</T>
          <FormFieldsWrapper>
            <EditingTextField
              label={t("entities.nickname")}
              name="nickname"
              onEdit={handleEditMe}
              initialValues={{ nickname: me?.nickname || "" }}
              validationSchema={() => getValidationSchema("nickname")}
            />
            <FormFieldsWrapper flexDirection={{ xs: "column", md: "row" }}>
              <EditingTextField
                label={t("entities.firstName")}
                name="first_name"
                onEdit={handleEditMe}
                initialValues={{ first_name: me?.first_name || "" }}
                validationSchema={() => getValidationSchema("first_name")}
              />
              <EditingTextField
                label={t("entities.lastName")}
                name="last_name"
                onEdit={handleEditMe}
                initialValues={{ last_name: me?.last_name || "" }}
                validationSchema={() => getValidationSchema("last_name")}
              />
            </FormFieldsWrapper>
          </FormFieldsWrapper>
        </Box>
      </Card>
      {isMobile && (
        <Button variant="outlined" color="error" onClick={handleLogout} sx={{ mt: "auto" }}>
          {t("actions.logout")}
        </Button>
      )}
    </PageContentWrapperStyled>
  );
});
