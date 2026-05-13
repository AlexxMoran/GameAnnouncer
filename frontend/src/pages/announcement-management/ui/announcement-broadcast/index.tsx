import { Card } from "@shared/ui/card";
import { observer } from "mobx-react-lite";
import type { FC } from "react";

export const AnnouncementBroadcast: FC = observer(() => {
  return <Card sx={{ height: "600px" }}></Card>;
});
