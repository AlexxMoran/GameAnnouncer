import { styled } from "@mui/material";

export const CardLabelStyled = styled("div")(({ theme }) => ({
  padding: `${theme.spacing(0.5)} ${theme.spacing(1.5)}`,
  width: "fit-content",
  position: "absolute",
  borderRadius: +theme.shape.borderRadius * 6 + "px",
  fontSize: theme.typography.caption.fontSize,
  fontWeight: theme.typography.caption.fontWeight,
  lineHeight: theme.typography.caption.lineHeight,
}));
