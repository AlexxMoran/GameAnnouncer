import type { IGameDto } from "@shared/services/api/games-api-service/types";
import type { IMenuAction } from "@shared/ui/actions-menu/types";

export interface IGameCardProps {
  game: IGameDto;
  actionList?: IMenuAction[];
}

export interface IGameImgStyledProps {
  imgUrl?: string;
}
