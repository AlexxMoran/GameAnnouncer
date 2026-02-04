import type { GamesApiService } from "@shared/services/api/games-api-service";
import type {
  ICreateGameDto,
  IEditGameDto,
  IGameDto,
  IGetGamesDto,
} from "@shared/services/api/games-api-service/types";
import { EntityCrudService } from "@shared/services/entity-crud-service";

export class GamesService extends EntityCrudService<IGameDto, IGetGamesDto, ICreateGameDto, IEditGameDto> {
  constructor(private gamesApiService: GamesApiService) {
    super({
      getEntitiesFn: gamesApiService.getGames,
      createEntityFn: gamesApiService.createGame,
      editEntityFn: gamesApiService.editGame,
      deleteEntityFn: gamesApiService.deleteGame,
    });
  }

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
