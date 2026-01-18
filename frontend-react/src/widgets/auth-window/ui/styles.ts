import styled from "@emotion/styled";

export const AuthFormWrapperStyled = styled("div")(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  justifyContent: "center",
  gap: theme.spacing(6),
  padding: theme.spacing(1),
  backgroundColor: theme.palette.background.paper,
  boxShadow: theme.shadows[8],
  borderRadius: +theme.shape.borderRadius * 6 + "px",
  paddingInline: theme.spacing(10),
  paddingBlock: theme.spacing(10),
  marginBottom: theme.spacing(20),
  maxWidth: "600px",
  minWidth: "400px",
  width: "45%",
}));
