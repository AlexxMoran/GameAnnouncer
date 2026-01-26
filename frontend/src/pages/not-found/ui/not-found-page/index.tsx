import { Box } from "@shared/ui/box";
import { T } from "@shared/ui/typography";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const NotFoundPage: FC = () => {
  const { t } = useTranslation();

  return (
    <Box height="100%" display="flex" alignItems="center" justifyContent="center">
      <T variant="h4">{t("texts.notFoundPage")}</T>
    </Box>
  );
};
