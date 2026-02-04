import { ListItemIcon, ListItemText, Menu, MenuItem } from "@mui/material";
import type { TMaybe } from "@shared/types/main.types";
import type { IActionsMenuProps } from "@shared/ui/actions-menu/types";
import { Tooltip } from "@shared/ui/tooltip";
import { createElement, useState, type FC } from "react";

export const ActionsMenu: FC<IActionsMenuProps> = (props) => {
  const { actionList } = props;
  const [isOpened, setIsOpened] = useState(false);
  const [ref, setRef] = useState<TMaybe<HTMLElement>>(null);

  const handleOpenMenu = () => {
    setIsOpened(true);
  };

  const handleCloseMenu = () => {
    setIsOpened(false);
  };

  const children = createElement(props.children, {
    onClick: handleOpenMenu,
    ref: setRef,
  });

  return (
    <>
      <Menu open={isOpened} anchorEl={ref} onClose={handleCloseMenu} disableScrollLock>
        {actionList.map((action) => {
          const { onClick, disabled, id, icon, title, tooltip } = action;

          const handleClickMenuItem = () => {
            onClick?.(id);
            handleCloseMenu();
          };

          return (
            <Tooltip key={id} title={tooltip} hidden={!tooltip}>
              <MenuItem onClick={handleClickMenuItem} disabled={disabled}>
                {icon && <ListItemIcon>{icon}</ListItemIcon>}
                <ListItemText>{title}</ListItemText>
              </MenuItem>
            </Tooltip>
          );
        })}
      </Menu>
      {children}
    </>
  );
};
