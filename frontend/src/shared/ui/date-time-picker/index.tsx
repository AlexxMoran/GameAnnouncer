import { useTheme } from "@mui/material";
import { DateTimePicker as MuiDateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import type { IDateTimePickerProps } from "@shared/ui/date-time-picker/types";
import { memo, type FC } from "react";

export const DateTimePicker: FC<IDateTimePickerProps> = memo((props) => {
  const theme = useTheme();

  return (
    <MuiDateTimePicker
      sx={{
        "& .MuiPickersOutlinedInput-root": {
          backgroundColor: "#22262C",
          borderRadius: 20,
          "& fieldset": {
            borderColor: theme.palette.divider,
          },
          "&.Mui-focused fieldset": {
            borderWidth: 1,
          },
          "&::first-letter": { textTransform: "capitalize" },
        },
      }}
      {...props}
      slotProps={{
        textField: {
          ...props.slotProps?.textField,
          size: "small",
        },
      }}
    />
  );
});
