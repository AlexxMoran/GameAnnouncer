import ExpandLessIcon from "@mui/icons-material/ExpandLess";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import PeopleIcon from "@mui/icons-material/People";
import { IconButton, useTheme } from "@mui/material";
import { CARD_HEIGHT } from "@pages/my-announcements/ui/announcement-card/constants";
import type { IAnnouncementCardProps } from "@pages/my-announcements/ui/announcement-card/types";
import { createAnnouncementStatusColor } from "@shared/helpers/createAnnouncementStatusColor";
import { prepareDate } from "@shared/helpers/prepareDate";
import { CardLabelStyled } from "@shared/ui/_styled/card-label-styled";
import { CardStyled } from "@shared/ui/_styled/card-styled";
import { EntityImgStyled } from "@shared/ui/_styled/entity-img-styled";
import { WithLineClampStyled } from "@shared/ui/_styled/with-line-clamp-styled";
import { ActionsMenu } from "@shared/ui/actions-menu";
import { Box } from "@shared/ui/box";
import { Collapse } from "@shared/ui/collapse";
import { T } from "@shared/ui/typography";
import { forwardRef, useState } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementCard = forwardRef<
  HTMLDivElement,
  IAnnouncementCardProps
>((props, ref) => {
  const { announcement, actionList } = props;

  const { t } = useTranslation();
  const theme = useTheme();
  const [isExpanded, setIsExpanded] = useState(false);

  const {
    image_url,
    title,
    content,
    participants_count,
    max_participants,
    status,
    registration_end_at,
    registration_start_at,
    start_at,
  } = announcement;

  const participantsInfo = `${participants_count} / ${max_participants}`;
  const statusColor = createAnnouncementStatusColor(theme, status);

  const moreInfoList = [
    { label: t("texts.announcementStartDate"), value: prepareDate(start_at) },
    {
      label: t("texts.registrationStartDate"),
      value: prepareDate(registration_start_at),
    },
    {
      label: t("texts.registrationEndDate"),
      value: prepareDate(registration_end_at),
    },
  ];

  const handleExpand = () => {
    setIsExpanded((value) => !value);
  };

  return (
    <Box display="flex" flexDirection="column" gap={2}>
      <CardStyled
        ref={ref}
        sx={{
          minHeight: CARD_HEIGHT,
          flexDirection: "row",
          gap: (theme) => theme.spacing(2),
        }}
      >
        <EntityImgStyled imgUrl={image_url} sx={{ maxHeight: CARD_HEIGHT }}>
          <CardLabelStyled
            sx={{
              backgroundColor: (theme) => theme.palette.secondary.main,
              bottom: (theme) => theme.spacing(2),
              left: (theme) => theme.spacing(2),
              gap: (theme) => theme.spacing(2),
              display: "flex",
              alignItems: "center",
            }}
          >
            <PeopleIcon fontSize="small" />
            {participantsInfo}
          </CardLabelStyled>
          <CardLabelStyled
            sx={{
              backgroundColor: statusColor,
              top: (theme) => theme.spacing(2),
              left: (theme) => theme.spacing(2),
            }}
          >
            {t(`enums.announcementStatuses.${status}`)}
          </CardLabelStyled>
        </EntityImgStyled>
        <Box display="flex" flexDirection="column" gap={2} px={3} flex={2}>
          <WithLineClampStyled lineClamp={1} variant="subtitle2">
            {title}
          </WithLineClampStyled>
          {content && (
            <WithLineClampStyled
              lineClamp={isExpanded ? undefined : 3}
              variant="caption"
            >
              {content}
            </WithLineClampStyled>
          )}
        </Box>
        <Box
          display="flex"
          flexDirection="column"
          justifyContent="space-between"
        >
          {actionList?.length && (
            <ActionsMenu actionList={actionList}>
              {({ onClick, ref }) => (
                <IconButton ref={ref} onClick={onClick}>
                  <MoreHorizIcon />
                </IconButton>
              )}
            </ActionsMenu>
          )}
          <IconButton sx={{ alignSelf: "end" }} onClick={handleExpand}>
            {isExpanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
          </IconButton>
        </Box>
      </CardStyled>
      <Collapse in={isExpanded}>
        <Box display="flex" gap={2}>
          <Box flex={1}></Box>
          <Box flex={2} px={3}>
            {moreInfoList.map(({ label, value }) => (
              <Box display="flex" gap={1}>
                <T variant="caption" sx={{ flex: 1 }}>
                  {label}:
                </T>
                <T variant="caption" sx={{ flex: 1 }}>
                  {value}
                </T>
              </Box>
            ))}
          </Box>
          <Box width={40} />
        </Box>
      </Collapse>
    </Box>
  );
});
