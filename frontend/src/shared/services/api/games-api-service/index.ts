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

  getGames = (params?: IGetGamesDto) => {
    return this.baseApiService.get<
      TApiResponseWrapper<IGameDto[]>,
      IPaginationMeta
    >(GAMES_ENDPOINT, { params });
  };

  createGame = (params: ICreateGameDto) => {
    return this.baseApiService.post<TApiResponseWrapper<IGameDto>>(
      GAMES_ENDPOINT,
      params
    );
  };

  editGame = (id: number, params: IEditGameDto) => {
    return this.baseApiService.patch<TApiResponseWrapper<IGameDto>>(
      `${GAMES_ENDPOINT}/${id}`,
      params
    );
  };

  deleteGame = (id: number) => {
    return this.baseApiService.delete<TApiResponseWrapper<IGameDto>>(
      `${GAMES_ENDPOINT}/${id}`
    );
  };

  uploadGameImage = (id: number, file: File) => {
    const formData = new FormData();

    formData.append("file", file);

    return this.baseApiService.post<TApiResponseWrapper<IGameDto>>(
      `${GAMES_ENDPOINT}/${id}/upload_image`,
      formData
    );
  };
}
