import { DatePicker as MuiDatePicker } from "@mui/x-date-pickers/DatePicker";
import type { IDatePickerProps } from "@shared/ui/date-picker/type";
import type { FC } from "react";

export const DatePicker: FC<IDatePickerProps> = (props) => {
  return (
    <MuiDatePicker
      {...props}
      slotProps={{
        ...props.slotProps?.textField,
        textField: { size: "small" },
      }}
    />
  );
};
