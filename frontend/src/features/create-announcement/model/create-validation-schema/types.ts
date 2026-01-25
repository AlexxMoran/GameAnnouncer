import type { ICreateAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import type { IGameDto } from "@shared/services/api/games-api-service/types";
import type { TMaybe } from "@shared/types/main.types";

export interface ICreateAnnouncementsFields
  extends Omit<ICreateAnnouncementDto, "game_id"> {
  game: TMaybe<IGameDto>;
}
