import type { IOutletContextData } from "@pages/announcement-management/model/types";
import { Card } from "@shared/ui/card";
import { observer } from "mobx-react-lite";
import type { FC } from "react";
import { useOutletContext } from "react-router";

export const AnnouncementRequests: FC = observer(() => {
  const outletContext = useOutletContext<IOutletContextData>();

  return <Card sx={{ height: "600px" }}></Card>;
});
