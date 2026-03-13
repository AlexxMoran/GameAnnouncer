import { useTheme } from "@mui/material";
import { MainPageImgContentStyled, MainPageImgStyled } from "@pages/announcements/ui/announcements-page/styles";
import { T } from "@shared/ui/typography";
import { type FC } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementsWelcomeImg: FC = () => {
  const { t } = useTranslation();
  const theme = useTheme();

  return (
    <MainPageImgStyled>
      <MainPageImgContentStyled>
        <T variant="h3" sx={{ maxWidth: { xs: "350px", md: "700px" } }}>
          {t("texts.mainTitleCompete")}{" "}
          <span style={{ color: theme.palette.primary.main }}>{t("texts.mainTitleWin")}</span>{" "}
          {t("texts.mainTitleImprove")}
        </T>
        <T variant="body2" sx={{ maxWidth: { xs: "350px", md: "550px" } }}>
          {t("texts.mainSubtitle")}
        </T>
      </MainPageImgContentStyled>
    </MainPageImgStyled>
  );
};
