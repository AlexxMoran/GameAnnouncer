import { Badge } from "@shared/ui/badge";
import type { IPageTitleProps } from "@shared/ui/page-title/types";
import { T } from "@shared/ui/typography";
import type { FC } from "react";

export const PageTitle: FC<IPageTitleProps> = ({ title, count, type = "page" }) => {
  return (
    <Badge badgeContent={count} color="secondary">
      <T variant={type === "page" ? "h4" : "h5"} sx={{ "&::first-letter": { textTransform: "capitalize" } }}>
        {title}
      </T>
    </Badge>
  );
};
