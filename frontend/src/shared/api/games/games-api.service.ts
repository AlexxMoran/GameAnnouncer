import { inject, Injectable } from '@angular/core';
import { TApiResponseWrapper } from '@shared/api/base-api-service.types';
import { BaseApiService } from '@shared/api/base-api.service';
import {
  ICreateGameDto,
  IEditGameDto,
  IGameDto,
  IGetGameListDto,
} from '@shared/api/games/games-api-service.types';
import { GAMES_ENDPOINT } from '@shared/api/games/games-api.constants';
import { IPaginationMeta } from '@shared/lib/pagination/pagination.types';

@Injectable({ providedIn: 'root' })
export class GamesApiService {
  private baseApiService = inject(BaseApiService);

  getGameList = (params?: IGetGameListDto) => {
    return this.baseApiService.get<TApiResponseWrapper<IGameDto[]>, IPaginationMeta>(
      GAMES_ENDPOINT,
      { params },
    );
  };

  createGame = (params: ICreateGameDto) => {
    return this.baseApiService.post<TApiResponseWrapper<IGameDto>>(GAMES_ENDPOINT, params);
  };

  editGame = (id: number, params: IEditGameDto) => {
    return this.baseApiService.patch<TApiResponseWrapper<IGameDto>>(
      `${GAMES_ENDPOINT}/${id}`,
      params,
    );
  };

  deleteGame = (id: number) => {
    return this.baseApiService.delete<TApiResponseWrapper<IGameDto>>(`${GAMES_ENDPOINT}/${id}`);
  };

  uploadGameImage = (id: number, file: File) => {
    const formData = new FormData();

    formData.append('file', file);

    return this.baseApiService.post<TApiResponseWrapper<IGameDto>>(
      `${GAMES_ENDPOINT}/${id}/upload_image`,
      formData,
    );
  };
}
