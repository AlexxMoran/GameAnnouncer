import { Tabs as MuiTabs, Tab } from "@mui/material";
import { Box } from "@shared/ui/box";
import type { ITabsProps } from "@shared/ui/tabs/types";
import { type FC } from "react";

export const Tabs: FC<ITabsProps> = ({ tabList, children, ...rest }) => {
  return (
    <Box height="100%" display="flex" flexDirection="column" gap={3}>
      <MuiTabs {...rest}>
        {tabList.map(({ label, value }) => (
          <Tab key={label} label={label} value={value} />
        ))}
      </MuiTabs>
      {children}
    </Box>
  );
};
