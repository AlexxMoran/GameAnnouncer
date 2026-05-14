import { AVATAR_ICONS } from "@shared/constants/avatars";
import { GAPS } from "@shared/constants/gaps";
import { useRootService } from "@shared/hooks/use-root-service";
import type { IEditUserDto } from "@shared/services/api/auth-api-service/types";
import { Avatar } from "@shared/ui/avatar";
import { Box } from "@shared/ui/box";
import { Card } from "@shared/ui/card";
import { PageTitle } from "@shared/ui/page-title";
import { T } from "@shared/ui/typography";
import type { FC } from "react";
import { useState } from "react";
import { HexColorPicker } from "react-colorful";
import { useTranslation } from "react-i18next";

export const AvatarSettings: FC = () => {
  const { t } = useTranslation();
  const { authApiService, authService } = useRootService();

  const { me, setMe } = authService;
  const { avatar_color, avatar_icon_id } = me || {};

  const [iconId, setIconId] = useState<keyof typeof AVATAR_ICONS | undefined>(
    avatar_icon_id && AVATAR_ICONS[avatar_icon_id as keyof typeof AVATAR_ICONS]
      ? (avatar_icon_id as keyof typeof AVATAR_ICONS)
      : undefined
  );

  const [color, setColor] = useState<string | undefined>(avatar_color ? avatar_color : undefined);
  const [isLoading, setIsLoading] = useState(false);

  const handleEditMe = async (values: IEditUserDto) => {
    setIsLoading(true);

    try {
      const { data } = await authApiService.editMe(values);

      setMe(data.data);

      return data;
    } catch (_) {
      /* empty */
    } finally {
      setIsLoading(false);
    }
  };

  const SelectedIcon = iconId ? AVATAR_ICONS[iconId] : undefined;

  const handleChangeColor = async (color: string) => {
    if (isLoading) return;

    const result = await handleEditMe({ avatar_color: color });

    if (result) {
      setColor(color);
    }
  };

  const handleChangeIcon = async (iconId: keyof typeof AVATAR_ICONS) => {
    if (isLoading) return;

    const result = await handleEditMe({ avatar_icon_id: iconId });

    if (result) {
      setIconId(iconId);
    }
  };

  return (
    <Card sx={{ p: GAPS }}>
      <Box display="flex" flexDirection="column" gap={GAPS} width={{ xs: "100%", md: "50%" }}>
        <Box>
          <PageTitle type="tab" title={t("entities.avatar.one")} />
          <T variant="body2" color="textSecondary">
            {t("texts.chooseIconAndColorForAvatar")}
          </T>
        </Box>
        <Avatar icon={SelectedIcon} color={color} isLoading={isLoading} size={80} />
        <Box display="flex" flexDirection="column" gap={1.5}>
          <T sx={{ "&::first-letter": { textTransform: "capitalize" } }} variant="subtitle1">
            {t("entities.icon.one")}
          </T>
          <Box display="flex" flexWrap="wrap" gap={1}>
            {Object.entries(AVATAR_ICONS).map(([id, Icon]) => (
              <Box
                key={id}
                sx={{
                  width: "52px",
                  height: "52px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  borderWidth: "1px",
                  cursor: "pointer",
                  borderStyle: "solid",
                  borderRadius: (theme) => theme.shape.borderRadius,
                  borderColor: (theme) => (+id === iconId ? theme.palette.primary.main : theme.palette.divider),
                  "@media (hover: hover) and (pointer: fine)": {
                    borderColor: (theme) => theme.palette.primary.main,
                  },
                }}
                onClick={() => handleChangeIcon(+id as keyof typeof AVATAR_ICONS)}
              >
                <Icon fontSize="large" />
              </Box>
            ))}
          </Box>
        </Box>
        <Box display="flex" flexDirection="column" gap={1.5}>
          <T sx={{ "&::first-letter": { textTransform: "capitalize" } }} variant="subtitle1">
            {t("entities.color.one")}
          </T>
          <HexColorPicker color={color} onChangeEnd={handleChangeColor} />
        </Box>
      </Box>
    </Card>
  );
};
