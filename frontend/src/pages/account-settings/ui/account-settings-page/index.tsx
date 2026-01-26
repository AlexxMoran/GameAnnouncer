import { createValidationSchema } from "@pages/account-settings/model/create-validation-schema";
import { EditingTextField } from "@pages/account-settings/ui/editing-text-field";
import { useRootService } from "@shared/hooks/use-root-service";
import type { IEditUserDto } from "@shared/services/api/auth-api-service/types";
import { CardStyled } from "@shared/ui/_styled/card-styled";
import { Box } from "@shared/ui/box";
import { T } from "@shared/ui/typography";
import { observer } from "mobx-react-lite";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const AccountSettingsPage: FC = observer(() => {
  const { t } = useTranslation();
  const { authApiService, authService } = useRootService();
  const { me, setMe } = authService;

  const handleEditMe = async (values: IEditUserDto) => {
    const { data } = await authApiService.editMe(values);

    setMe(data.data);
  };

  const getValidationSchema = (name: keyof IEditUserDto) => {
    return createValidationSchema(name, t);
  };

  return (
    <Box display="flex" flexDirection="column" gap={8} height="100%">
      <T variant="h4">{t("texts.accountSettings")}</T>
      <CardStyled sx={{ p: (theme) => theme.spacing(8), flex: 1 }}>
        <Box display="flex" flexDirection="column" gap={8} width="50%" minWidth="250px">
          <T variant="h6">{t("texts.usersData")}</T>
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
          <EditingTextField
            label={t("entities.nickname")}
            name="nickname"
            onEdit={handleEditMe}
            initialValues={{ nickname: me?.nickname || "" }}
            validationSchema={() => getValidationSchema("nickname")}
          />
        </Box>
      </CardStyled>
    </Box>
  );
});
