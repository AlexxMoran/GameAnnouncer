import type { IEntityCrudServiceParams } from "@shared/services/entity-crud-service/types";
import { PaginationService } from "@shared/services/pagination-service";
import type {
  IEntityIdField,
  TEntityId,
} from "@shared/types/commonEntity.types";
import type { IPaginationParams } from "@shared/types/pagination.types";

export class EntityCrudService<
  TEntity extends IEntityIdField,
  TGetListParams extends IPaginationParams,
  TCreateParams = never,
  TEditParams = never,
> {
  paginationService: PaginationService<TEntity, TGetListParams>;

  constructor(
    private params: IEntityCrudServiceParams<
      TEntity,
      TGetListParams,
      TCreateParams,
      TEditParams
    >,
  ) {
    const paginationService = new PaginationService({
      loadFn: params.getEntitiesFn,
    });

    this.paginationService = paginationService;

    paginationService.init();
  }

  createEntity = async (params: TCreateParams) => {
    try {
      const result = await this.params.createEntityFn?.(params);

      if (result) {
        this.paginationService.init();
      }

      return result;
    } catch (_) {
      /* empty */
    }
  };

  editEntity = async (gameId: TEntityId, params: TEditParams) => {
    try {
      const result = await this.params.editEntityFn?.(gameId, params);

      if (result) {
        const { data } = result;

        this.paginationService.setItem(data.data);

        return data;
      }
    } catch (_) {
      /* empty */
    }
  };

  deleteEntity = async (gameId: number) => {
    try {
      const result = await this.params.deleteEntityFn?.(gameId);

      if (result) {
        this.paginationService.init();

        return result;
      }
    } catch (_) {
      /* empty */
    }
  };
}
