import { createValidationSchema } from "@pages/account-settings/model/create-validation-schema";
import { EditingTextField } from "@pages/account-settings/ui/editing-text-field";
import { GAPS } from "@shared/constants/gaps";
import { useRootService } from "@shared/hooks/use-root-service";
import type { IEditUserDto } from "@shared/services/api/auth-api-service/types";
import { Box } from "@shared/ui/box";
import { Card } from "@shared/ui/card";
import { FormFieldsWrapper } from "@shared/ui/form/form-fields-wrapper";
import { PageTitle } from "@shared/ui/page-title";
import { type FC } from "react";
import { useTranslation } from "react-i18next";

export const UserInfoSettings: FC = () => {
  const { t } = useTranslation();
  const { authApiService, authService } = useRootService();

  const { me, setMe } = authService;

  const handleEditMe = async (values: IEditUserDto) => {
    try {
      const { data } = await authApiService.editMe(values);

      setMe(data.data);
    } catch (_) {
      /* empty */
    }
  };

  const getValidationSchema = (name: keyof IEditUserDto) => {
    return createValidationSchema(name, t);
  };

  return (
    <Card sx={{ p: GAPS }}>
      <Box display="flex" flexDirection="column" gap={GAPS} width={{ xs: "100%", md: "50%" }}>
        <PageTitle type="tab" title={t("texts.usersData")} />
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
  );
};
