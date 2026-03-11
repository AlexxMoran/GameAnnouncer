import { styled } from "@mui/material";
import { Card } from "@shared/ui/card";

export const AuthFormWrapperStyled = styled(Card)(({ theme }) => ({
  alignItems: "center",
  justifyContent: "center",
  gap: theme.spacing(6),
  padding: theme.spacing(1),
  backgroundColor: theme.palette.background.paper,
  borderRadius: +theme.shape.borderRadius * 6 + "px",
  // paddingInline: theme.spacing(10),
  // paddingBlock: theme.spacing(10),
  // marginBottom: theme.spacing(20),
  // maxWidth: "600px",
  // minWidth: "400px",
  width: "45%",
}));
