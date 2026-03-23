import { BottomBar } from "@app/bottom-bar";
import { TopBar } from "@app/top-bar";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import AssignmentIcon from "@mui/icons-material/Assignment";
import EmojiEventsIcon from "@mui/icons-material/EmojiEvents";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import StarIcon from "@mui/icons-material/Star";
import { useScrollTrigger } from "@mui/material";
import { EAppRoutes } from "@shared/constants/appRoutes";
import { useDeviceType } from "@shared/hooks/use-device-type";
import { Box } from "@shared/ui/box";
import { Fab } from "@shared/ui/fab-button";
import { Zoom } from "@shared/ui/zoom";
import { type FC, type PropsWithChildren } from "react";
import { useTranslation } from "react-i18next";

export const Layout: FC<PropsWithChildren> = ({ children }) => {
  const { t } = useTranslation();
  const { isMobile } = useDeviceType();

  const trigger = useScrollTrigger({
    disableHysteresis: true,
    threshold: 1000,
  });

  const handleScrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const navItemList = (() => {
    const list = [
      {
        label: t("entities.announcement.many"),
        icon: <EmojiEventsIcon />,
        url: EAppRoutes.Announcements,
      },
      {
        label: t("texts.myAnnouncementsTitle"),
        icon: <StarIcon />,
        url: EAppRoutes.MyAnnouncements,
      },
      {
        label: t("entities.bid.many"),
        icon: <AssignmentIcon />,
        url: EAppRoutes.RegistrationRequests,
      },
    ];

    if (isMobile) {
      list.push({
        label: t("entities.account.one"),
        icon: <AccountCircleIcon />,
        url: EAppRoutes.AccountSettings,
      });
    }

    return list;
  })();

  return (
    <Box display="flex" flexDirection="column" height="100%">
      <TopBar navItemList={navItemList} />
      {children}
      {isMobile && <BottomBar navItemList={navItemList} />}
      <Zoom in={trigger}>
        <Fab
          onClick={handleScrollToTop}
          sx={{
            position: "fixed",
            bottom: { xs: 72, md: 32 },
            right: { xs: 16, md: 32 },
          }}
          size={isMobile ? "small" : "medium"}
        >
          <KeyboardArrowUpIcon />
        </Fab>
      </Zoom>
    </Box>
  );
};
