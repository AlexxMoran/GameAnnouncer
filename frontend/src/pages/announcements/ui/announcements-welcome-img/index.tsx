import { useTheme } from "@mui/material";
import { MainPageImgContentStyled } from "@shared/ui/_styled/main-page-img-content-style";
import { MainPageImgStyled } from "@shared/ui/_styled/main-page-img-styled";
import { T } from "@shared/ui/typography";
import { type FC } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementsWelcomeImg: FC = () => {
  const { t } = useTranslation();
  const theme = useTheme();

  return (
    <MainPageImgStyled imgUrl="/src/shared/assets/images/main.jpeg" backgroundPosition="60% 65%">
      <MainPageImgContentStyled>
        <T variant="h3" sx={{ maxWidth: { xs: "350px", md: "700px" }, hyphens: "unset" }}>
          {t("texts.mainTitleCompete")}{" "}
          <span style={{ color: theme.palette.primary.main }}>{t("texts.mainTitleWin")}</span>{" "}
          {t("texts.mainTitleImprove")}
        </T>
        <T variant="body2" color="textSecondary" sx={{ maxWidth: { xs: "350px", md: "550px" }, hyphens: "unset" }}>
          {t("texts.mainSubtitle")}
        </T>
      </MainPageImgContentStyled>
    </MainPageImgStyled>
  );
};
