import { CardStyled } from "@shared/ui/_styled/card-styled";
import { Box } from "@shared/ui/box";
import { TabsStyled, TabStyled } from "@shared/ui/tabs/styles";
import type { ITabsProps } from "@shared/ui/tabs/types";
import { type FC } from "react";

export const Tabs: FC<ITabsProps> = ({ tabList, children, ...rest }) => {
  return (
    <Box height="100%" display="flex" flexDirection="column">
      <TabsStyled {...rest}>
        {tabList.map(({ label, value }) => (
          <TabStyled key={label} label={label} value={value} />
        ))}
      </TabsStyled>
      <CardStyled
        sx={{
          p: (theme) => theme.spacing(8),
          borderTopLeftRadius: 0,
          flex: 1,
        }}
      >
        {children}
      </CardStyled>
    </Box>
  );
};
