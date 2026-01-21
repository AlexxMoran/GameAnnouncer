import type { GamesApiService } from "@shared/services/api/games-api-service";
import type {
  ICreateGameDto,
  IEditGameDto,
  IGameDto,
  IGetGameListDto,
} from "@shared/services/api/games-api-service/types";
import { PaginationService } from "@shared/services/pagination-service";

export class GamesService {
  paginationService: PaginationService<IGameDto, IGetGameListDto>;

  constructor(private gamesApiService: GamesApiService) {
    const paginationService = new PaginationService({
      loadFn: this.gamesApiService.getGameList,
    });

    this.paginationService = paginationService;

    paginationService.init();
  }

  createGame = async (params: ICreateGameDto) => {
    try {
      const result = await this.gamesApiService.createGame(params);

      if (result) {
        this.paginationService.init();
      }

      return result;
    } catch (_) {
      /* empty */
    }
  };

  editGame = async (gameId: number, params: IEditGameDto) => {
    try {
      const { data } = await this.gamesApiService.editGame(gameId, params);

      if (data) {
        this.paginationService.setItem(data.data);
      }

      return data;
    } catch (_) {
      /* empty */
    }
  };

  deleteGame = async (gameId: number) => {
    try {
      const result = await this.gamesApiService.deleteGame(gameId);

      if (result) {
        this.paginationService.init();
      }

      return result;
    } catch (_) {
      /* empty */
    }
  };

  uploadGameImage = async (id: number, image: File) => {
    try {
      const { data } = await this.gamesApiService.uploadGameImage(id, image);

      if (data) {
        this.paginationService.setItem(data.data);
      }

      return data;
    } catch (_) {
      /* empty */
    }
  };
}
