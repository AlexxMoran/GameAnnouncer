import { DEFAULT_PAGINATION_LIMIT } from "@shared/services/pagination-service/constants";
import type {
  IPaginationServiceParams,
  TEntityId,
} from "@shared/services/pagination-service/types";
import type { TMaybe, TObjectAny } from "@shared/types/main.types";
import { makeAutoObservable, runInAction } from "mobx";

export class PaginationService<TEntity extends TObjectAny & { id: TEntityId }> {
  private listMap = new Map<TEntityId, TEntity>();

  limit = DEFAULT_PAGINATION_LIMIT;
  total: TMaybe<number> = null;

  isPaginating = false;
  isInitialLoading = false;
  hasDataToLoad = true;

  constructor(private params: IPaginationServiceParams<TEntity>) {
    makeAutoObservable(this);
  }

  private get paginationParams() {
    return { skip: this.list.length, limit: this.limit };
  }

  get list() {
    return Array.from(this.listMap.values());
  }

  private setList = (list: TEntity[]) => {
    list.forEach((entity) => this.setItem(entity));
  };

  setItem = (entity: TEntity) => {
    this.listMap.set(entity.id, entity);
  };

  paginate = async () => {
    try {
      if (this.isPaginating || this.isInitialLoading || !this.hasDataToLoad)
        return;

      this.isPaginating = true;

      const { data } = await this.params.loadFn(this.paginationParams);

      if (data) {
        const { total, data: list } = data;

        runInAction(() => {
          this.setList(list);
          this.total = total;
          this.hasDataToLoad = this.list.length < total;
        });
      }
    } finally {
      runInAction(() => (this.isPaginating = false));
    }
  };

  init = async () => {
    try {
      this.listMap.clear();
      this.isInitialLoading = true;

      const { data } = await this.params.loadFn(this.paginationParams);

      if (data) {
        const { total, data: list } = data;

        runInAction(() => {
          this.setList(list);
          this.total = total;
          this.hasDataToLoad = list.length < total;
        });
      }
    } catch (_) {
      runInAction(() => (this.total = 0));
    } finally {
      runInAction(() => (this.isInitialLoading = false));
    }
  };
}
