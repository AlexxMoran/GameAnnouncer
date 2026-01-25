import { DateTimePickerStyled } from "@shared/ui/date-time-picker/styles";
import type { IDateTimePickerProps } from "@shared/ui/date-time-picker/type";
import type { FC } from "react";

export const DateTimePicker: FC<IDateTimePickerProps> = (props) => {
  return (
    <DateTimePickerStyled
      {...props}
      slotProps={{
        textField: {
          ...props.slotProps?.textField,
          size: "small",
        },
      }}
    />
  );
};
