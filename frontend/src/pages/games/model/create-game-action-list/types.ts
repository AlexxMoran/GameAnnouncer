import type { IGameDto } from "@shared/services/api/games-api-service/types";
import type { TFunction } from "i18next";

export interface ICreateGameActionListParams {
  t: TFunction;
  game: IGameDto;
  handleOpenEditDialog: (game: IGameDto) => void;
  handleOpenUploadImageDialog: (game: IGameDto) => void;
  handleDeleteGame: (game: IGameDto) => void;
}
