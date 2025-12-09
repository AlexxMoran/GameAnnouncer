import { inject, Injectable } from '@angular/core';
import { BaseApiService } from '@shared/api/base-api.service';
import { GAMES_ENDPOINT } from '@shared/api/games/games-api.const';
import { IGameDto, IGetGameListDto } from '@shared/api/games/games-api.types';
import { IPaginationMeta } from '@shared/lib/pagination/pagination.types';

@Injectable({ providedIn: 'root' })
export class GamesApiService {
  private baseApiService = inject(BaseApiService);

  getGameList(params?: IGetGameListDto) {
    return this.baseApiService.get<IGameDto[], IPaginationMeta>(GAMES_ENDPOINT, params);
  }
}
