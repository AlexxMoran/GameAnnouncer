import { BottomBarStyled } from "@app/bottom-bar/styles";
import type { IBottomBarProps } from "@app/bottom-bar/types";
import { BottomNavigation, BottomNavigationAction } from "@mui/material";
import { Link } from "@shared/ui/link";
import type { FC } from "react";
import { useTranslation } from "react-i18next";
import { useLocation } from "react-router";

export const BottomBar: FC<IBottomBarProps> = ({ navItemList }) => {
  const { pathname } = useLocation();
  const { t } = useTranslation();

  const currentIndex = navItemList.findIndex((item) => {
    return pathname.startsWith(item.url);
  });

  return (
    <BottomBarStyled>
      <BottomNavigation value={currentIndex === -1 ? 0 : currentIndex} sx={{ backgroundColor: "initial" }} showLabels>
        {navItemList.map(({ url, label, icon }) => (
          <BottomNavigationAction key={url} label={t(label)} icon={icon} component={Link} to={url} />
        ))}
      </BottomNavigation>
    </BottomBarStyled>
  );
};
