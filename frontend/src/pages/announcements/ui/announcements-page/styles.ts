import { styled } from "@mui/material";

export const MainPageImgStyled = styled("div")`
  position: relative;
  background-image: url("/src/shared/assets/images/main.jpeg");
  background-repeat: no-repeat;
  background-size: cover;
  width: 100%;
  padding-top: min(calc(100% / 1.5), 340px);
  background-position: top;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(180deg, rgba(26, 30, 36, 0.75) 0%, rgba(20, 24, 28, 0.92) 100%);
  }
`;

export const MainPageImgContentStyled = styled("div")(({ theme }) => ({
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  maxWidth: "1280px",
  width: "100%",
  height: "100%",
  gap: theme.spacing(1.5),
  paddingInline: theme.spacing(2),
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",

  [theme.breakpoints.up("sm")]: {
    paddingInline: theme.spacing(3),
  },
}));
