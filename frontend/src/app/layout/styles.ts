import { styled } from "@mui/material";

export const HeaderStyled = styled("header")`
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  min-height: 48px;
  padding-inline: ${({ theme }) => theme.spacing(8)};
  display: flex;
  align-items: center;
  background-color: ${({ theme }) => theme.palette.background.paper};
  z-index: ${({ theme }) => theme.zIndex.appBar};
  position: sticky;
  top: 0;
`;

export const LayoutStyled = styled("div")(({ theme }) => ({
  maxWidth: "1280px",
  width: "100%",
  marginLeft: "auto",
  marginRight: "auto",
  paddingInline: theme.spacing(8),
  paddingBlock: theme.spacing(10),
  flex: "1 1 0%",
  position: "relative",
}));
