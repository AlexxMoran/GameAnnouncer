import type { IEntityCrudServiceParams } from "@shared/services/entity-crud-service/types";
import { FilterService } from "@shared/services/filter-service";
import { PaginationService } from "@shared/services/pagination-service";
import type { IEntityIdField, TEntityId } from "@shared/types/commonEntity.types";
import type { IPaginationParams } from "@shared/types/pagination.types";
import debounce from "lodash/debounce";
import { reaction, type IReactionDisposer } from "mobx";

export class EntityCrudService<
  TEntity extends IEntityIdField,
  TGetListParams extends IPaginationParams,
  TCreateParams = never,
  TEditParams = never,
> {
  private paginationService: PaginationService<TEntity, TGetListParams>;
  private filterService = new FilterService<TGetListParams>();
  reactionList: IReactionDisposer[] = [];

  constructor(private params: IEntityCrudServiceParams<TEntity, TGetListParams, TCreateParams, TEditParams>) {
    const paginationService = new PaginationService({
      loadFn: params.getEntitiesFn,
    });

    this.paginationService = paginationService;

    this.reactionList.push(
      reaction(
        () => this.filterService.filters,
        debounce((filters) => {
          paginationService.init(filters);
        }, 300)
      )
    );

    paginationService.init(this.filterService.filters);
  }

  get listData() {
    return {
      list: this.paginationService.list,
      isInitialLoading: this.paginationService.isInitialLoading,
      isPaginating: this.paginationService.isPaginating,
      total: this.paginationService.total,
    };
  }

  get filters() {
    return this.filterService.filters;
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

  paginate = async () => {
    await this.paginationService.paginate(this.filterService.filters);
  };

  setFilters = (filters: TGetListParams) => {
    this.filterService.setFilters(filters);
  };

  setFilter = <K extends keyof TGetListParams>(key: K, value: TGetListParams[K]) => {
    this.filterService.setFilter(key, value);
  };
}
