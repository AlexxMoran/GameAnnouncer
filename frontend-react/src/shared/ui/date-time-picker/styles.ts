import styled from "@emotion/styled";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";

export const DateTimePickerStyled = styled(DateTimePicker)`
  & label {
    display: inline-block;

    &::first-letter {
      text-transform: uppercase;
    }
  }
`;
