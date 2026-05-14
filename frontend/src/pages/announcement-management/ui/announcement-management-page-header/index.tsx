import { createAnnouncementStatusColor } from "@entities/announcement/lib/create-announcement-status-color";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import SportsEsportsIcon from "@mui/icons-material/SportsEsports";
import { useTheme } from "@mui/material";
import type { IAnnouncementManagementPageHeaderProps } from "@pages/announcement-management/ui/announcement-management-page-header/types";
import { MainPageImgContentStyled } from "@shared/ui/_styled/main-page-img-content-style";
import { MainPageImgStyled } from "@shared/ui/_styled/main-page-img-styled";
import { Box } from "@shared/ui/box";
import { Chip } from "@shared/ui/chip";
import { IconButton } from "@shared/ui/icon-button";
import { T } from "@shared/ui/typography";
import { observer } from "mobx-react-lite";
import type { FC } from "react";
import { useTranslation } from "react-i18next";
import { useLocation, useNavigate } from "react-router";

export const AnnouncementManagementPageHeader: FC<IAnnouncementManagementPageHeaderProps> = observer(
  ({ announcement }) => {
    const { t } = useTranslation();
    const location = useLocation();
    const navigate = useNavigate();
    const theme = useTheme();

    const showBackButton = location.key !== "default";

    const { game, status, title } = announcement || {};
    const { image_url, name } = game || {};

    const statusColor = createAnnouncementStatusColor(theme, status);

    const handleGoBack = () => {
      navigate(-1);
    };

    return (
      <MainPageImgStyled imgUrl={image_url || ""} backgroundPosition="center">
        <MainPageImgContentStyled sx={{ justifyContent: "flex-end", pb: { xs: 3, md: 4 } }}>
          {showBackButton && (
            <IconButton size="large" sx={{ alignSelf: "self-start" }} onClick={handleGoBack}>
              <ArrowBackIcon />
            </IconButton>
          )}
          <Box display="flex" gap={1.5}>
            <Chip
              label={t(`enums.announcementStatuses.${status}`)}
              sx={{
                color: (theme) => theme.palette.getContrastText(statusColor),
                backgroundColor: statusColor,
              }}
            />
            <Chip
              icon={<SportsEsportsIcon />}
              label={name}
              sx={{
                backgroundColor: (theme) => theme.palette.background.accent,
              }}
            />
          </Box>
          <T variant="h3">{title}</T>
        </MainPageImgContentStyled>
      </MainPageImgStyled>
    );
  }
);
