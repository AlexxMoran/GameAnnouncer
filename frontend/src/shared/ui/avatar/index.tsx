import { useTheme } from "@mui/material";
import type { IAvatarProps } from "@shared/ui/avatar/types";
import { Box } from "@shared/ui/box";
import { Spinner } from "@shared/ui/spinner";
import { T } from "@shared/ui/typography";
import { findContrastColor } from "color-contrast-finder";
import type { FC } from "react";

export const Avatar: FC<IAvatarProps> = ({ color, icon: Icon, isLoading, size = 40, username }) => {
  const theme = useTheme();

  const preparedColor = color ? findContrastColor({ color }) : undefined;

  return (
    <Box
      sx={{
        height: size,
        width: size,
        bgcolor: color || theme.palette.background.paper,
        borderRadius: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        border: (theme) => theme.palette.divider,
        borderColor: (theme) => theme.palette.divider,
        borderStyle: "solid",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {Icon ? (
        <Icon htmlColor={preparedColor} sx={{ fontSize: size / 1.5 }} />
      ) : username ? (
        <T sx={{ color: preparedColor }} fontSize={size / 1.5}>
          {username[0]}
        </T>
      ) : null}
      {isLoading && (
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: "100%",
            height: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Spinner />
        </Box>
      )}
    </Box>
  );
};
