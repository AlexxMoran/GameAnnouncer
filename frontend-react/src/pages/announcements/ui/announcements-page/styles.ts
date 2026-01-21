import { styled } from "@mui/material";

export const AnnouncementsWrapperStyled = styled("div")(({ theme }) => ({
  display: "grid",
  gap: theme.spacing(8),
  position: "relative",
  gridTemplateColumns: "1fr",

  [theme.breakpoints.up("sm")]: {
    gridTemplateColumns: "repeat(2, 1fr)",
  },

  [theme.breakpoints.up("lg")]: {
    gridTemplateColumns: "repeat(3, 1fr)",
  },
}));

export const MainPageImgStyled = styled("div")`
  position: relative;
  background-image: url("/src/shared/assets/images/announcements-main-img.png");
  background-repeat: no-repeat;
  background-size: cover;
  width: 100%;
  padding-top: calc(100% / (1136 / 456));
`;
