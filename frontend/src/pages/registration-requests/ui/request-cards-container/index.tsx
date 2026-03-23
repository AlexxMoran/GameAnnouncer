import { Box } from "@shared/ui/box";
import type { FC, PropsWithChildren } from "react";

export const RequestCardsContainer: FC<PropsWithChildren> = ({ children }) => {
  return (
    <Box display="flex" flexDirection="column" gap={2}>
      {children}
    </Box>
  );
};
