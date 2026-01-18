import styled from "@emotion/styled";

export const HeaderStyled = styled.header`
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  min-height: 48px;
  padding: 0 40px;
  display: flex;
  align-items: center;
  background-color: ${({ theme }) => theme.palette.background.paper};
  box-shadow: ${({ theme }) => theme.shadows[5]};
  z-index: ${({ theme }) => theme.zIndex.appBar};
  position: sticky;
  top: 0;
`;

export const LayoutStyled = styled("div")(({ theme }) => ({
  maxWidth: "1280px",
  width: "100%",
  marginLeft: "auto",
  marginRight: "auto",
  paddingLeft: theme.spacing(10),
  paddingRight: theme.spacing(10),
  paddingTop: theme.spacing(10),
  paddingBottom: theme.spacing(15),
  flex: "1 1 0%",
  position: "relative",
}));
