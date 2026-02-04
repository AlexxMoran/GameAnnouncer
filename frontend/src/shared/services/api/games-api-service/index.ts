import type { BaseApiService } from "@shared/services/api/base-api-service";
import type { TApiResponseWrapper } from "@shared/services/api/base-api-service/types";
import { GAMES_ENDPOINT } from "@shared/services/api/games-api-service/constants";
import type {
  ICreateGameDto,
  IEditGameDto,
  IGameDto,
  IGetGamesDto,
} from "@shared/services/api/games-api-service/types";
import type { IPaginationMeta } from "@shared/types/pagination.types";

export class GamesApiService {
  constructor(private baseApiService: BaseApiService) {}

  getGame = (id: number) => this.baseApiService.get<TApiResponseWrapper<IGameDto>>(`v1/${GAMES_ENDPOINT}/${id}`);

  getGames = (params?: IGetGamesDto) =>
    this.baseApiService.get<TApiResponseWrapper<IGameDto[]>, IPaginationMeta>(`v1/${GAMES_ENDPOINT}`, { params });

  createGame = (params: ICreateGameDto) =>
    this.baseApiService.post<TApiResponseWrapper<IGameDto>>(`v1/${GAMES_ENDPOINT}`, params);

  editGame = (id: number, params: IEditGameDto) =>
    this.baseApiService.patch<TApiResponseWrapper<IGameDto>>(`v1/${GAMES_ENDPOINT}/${id}`, params);

  deleteGame = (id: number) => this.baseApiService.delete<TApiResponseWrapper<IGameDto>>(`v1/${GAMES_ENDPOINT}/${id}`);

  uploadGameImage = (id: number, file: File) => {
    const formData = new FormData();

    formData.append("file", file);

    return this.baseApiService.post<TApiResponseWrapper<IGameDto>>(`v1/${GAMES_ENDPOINT}/${id}/upload_image`, formData);
  };
}
