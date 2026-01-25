import { styled } from "@mui/material";
import { CardStyled } from "@shared/ui/_styled/card-styled";
import type { IEntityCardStyledProps } from "@shared/ui/_styled/entity-card-styled/types";

export const EntityCardStyled = styled(CardStyled)<IEntityCardStyledProps>(
  ({ theme, withPointer, withBorder }) => {
    const baseStyles = {
      gap: theme.spacing(2),
      padding: theme.spacing(1),
      boxShadow: "none",
      width: "100%",
    };

    const pointerStyles = {
      transition: "transform 0.3s ease, box-shadow 0.3s ease",
      cursor: "pointer",

      "&:hover": {
        boxShadow: theme.shadows[16],
        transform: "scale(1.03)",
      },
    };

    const borderStyles = {
      border: `1px solid ${theme.palette.divider}`,
    };

    return Object.assign(
      {},
      baseStyles,
      withPointer && pointerStyles,
      withBorder && borderStyles
    );
  }
);
