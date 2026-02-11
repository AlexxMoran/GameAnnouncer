import type { IRegistrationFormOptionProps } from "@features/create-announcement/ui/registration-form-option/types";
import DeleteOutlinedIcon from "@mui/icons-material/DeleteOutlined";
import { Box } from "@shared/ui/box";
import { IconButton } from "@shared/ui/icon-button";
import { TextField } from "@shared/ui/text-field";
import { Tooltip } from "@shared/ui/tooltip";
import { memo, type FC } from "react";
import { useTranslation } from "react-i18next";

export const RegistrationFormOption: FC<IRegistrationFormOptionProps> = memo((props) => {
  const { fieldKey, optionKey, isDeletionDisabled, optionValue, error, onChangeOption, onDeleteOption } = props;

  const { t } = useTranslation();

  return (
    <Box display="flex" gap={2} key={optionKey}>
      <TextField
        sx={{ flex: 1 }}
        value={optionValue}
        onChange={(event) => onChangeOption?.(event, fieldKey, optionKey)}
        error={!!error}
        helperText={error}
      />
      <Tooltip title={t("actions.deleteOption")}>
        <IconButton
          sx={{ alignSelf: "center" }}
          disabled={isDeletionDisabled}
          onClick={() => onDeleteOption?.(fieldKey, optionKey)}
        >
          <DeleteOutlinedIcon />
        </IconButton>
      </Tooltip>
    </Box>
  );
});
