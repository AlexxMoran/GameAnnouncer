import { inject, Injectable, InjectionToken, signal } from '@angular/core';
import { BaseApiService } from '@shared/lib/api/base-api.service';
import { IPaginationParams } from '@shared/lib/api/offset-pagination.types';
import { TObjectAny } from '@shared/lib/utility-types/object.types';

export const ENDPOINT_URL = new InjectionToken<string>('endpoint-url');
export const PAGINATION_LIMIT = new InjectionToken<number | undefined>('pagination-limit');

type THasOffsetPaginationMeta = true;

@Injectable()
export class OffsetPaginationService<TEntity extends TObjectAny> {
  private baseApiService = inject(BaseApiService);
  private url = inject(ENDPOINT_URL);
  private limit = signal(inject(PAGINATION_LIMIT, { optional: true }) || 25);
  private skip = signal(0);
  private totalCount = signal(0);
  list = signal<TEntity[]>([]);
  isInitializeLoading = signal(false);
  isPaginating = signal(false);

  get canPaginate() {
    return this.list().length < this.totalCount();
  }

  private loadData(paginationParams: IPaginationParams) {
    const isNext = paginationParams.skip > 0;

    this.setLoading(isNext, true);

    this.baseApiService
      .get<TEntity[], THasOffsetPaginationMeta>(this.url, paginationParams)
      .subscribe({
        next: ({ data, total_count }) => {
          if (isNext) {
            this.list.update((list) => [...list, ...data]);
          } else {
            this.list.set(data);
          }

          this.totalCount.set(total_count);
          this.skip.set(paginationParams.skip);
          this.setLoading(isNext, false);
        },
        error: (error) => {
          console.error(error);

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
    if (this.canPaginate) {
      this.loadData({ limit: this.limit(), skip: this.skip() + 1 });
    }
  }
}
