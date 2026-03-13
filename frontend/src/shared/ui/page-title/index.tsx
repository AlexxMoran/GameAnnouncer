import { Badge } from "@shared/ui/badge";
import type { IPageTitleProps } from "@shared/ui/page-title/types";
import { T } from "@shared/ui/typography";
import type { FC } from "react";

export const PageTitle: FC<IPageTitleProps> = ({ title, count }) => {
  return (
    <Badge badgeContent={count} color="secondary">
      <T variant="h4" className="capitalize-first">
        {title}
      </T>
    </Badge>
  );
};
