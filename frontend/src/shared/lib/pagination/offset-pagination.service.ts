import { computed, signal } from '@angular/core';
import {
  IPaginationConfig,
  IPaginationParams,
  TLoadDataFn,
} from '@shared/lib/pagination/offset-pagination.types';
import { TObjectAny } from '@shared/lib/utility-types/object.types';

export class OffsetPaginationService<TEntity extends TObjectAny> {
  private loadDataFn: TLoadDataFn<TEntity>;
  private limit = signal(25);
  private skip = signal(0);
  private totalCount = signal(0);
  list = signal<TEntity[]>([]);
  isInitializeLoading = signal(false);
  isPaginating = signal(false);

  constructor(config: IPaginationConfig<TEntity>) {
    this.loadDataFn = config.loadDataFn;

    if (config.limit) {
      this.limit.set(config.limit);
    }
  }

  canPaginate = computed(() => this.list().length < this.totalCount() && !this.isPaginating());

  private loadData(paginationParams: IPaginationParams) {
    const isNext = paginationParams.skip > 0;

    this.setLoading(isNext, true);

    this.loadDataFn(paginationParams).subscribe({
      next: ({ data, total }) => {
        if (isNext) {
          this.list.update((list) => [...list, ...data]);
        } else {
          this.list.set(data);
        }

        this.totalCount.set(total);
        this.skip.set(paginationParams.skip);
        this.setLoading(isNext, false);
      },
      error: () => {
        this.setLoading(isNext, false);
      },
    });
  }

  private setLoading(isNext: boolean, value: boolean) {
    if (isNext) {
      this.isPaginating.set(value);
    } else {
      this.isInitializeLoading.set(value);
    }
  }

  initDataLoading() {
    this.loadData({ limit: this.limit(), skip: 0 });
  }

  paginate() {
    if (this.canPaginate()) {
      this.loadData({ limit: this.limit(), skip: this.skip() + 1 });
    }
  }
}
