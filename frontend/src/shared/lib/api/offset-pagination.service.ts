import { computed, inject, Injectable, InjectionToken, signal } from '@angular/core';
import { BaseApiService } from '@shared/lib/api/base-api.service';
import { IPaginationParams } from '@shared/lib/api/offset-pagination.types';
import { TObjectAny } from '@shared/lib/utility-types/object.types';

export const ENDPOINT = new InjectionToken<string>('endpoint');
export const PAGINATION_LIMIT = new InjectionToken<number | undefined>('pagination-limit');

@Injectable()
export class OffsetPaginationService<TEntity extends TObjectAny> {
  private baseApiService = inject(BaseApiService);
  private url = inject(ENDPOINT);
  private limit = signal(inject(PAGINATION_LIMIT, { optional: true }) || 10);
  private skip = signal(0);
  private totalCount = signal(0);
  list = signal<TEntity[]>([]);
  isInitializeLoading = signal(false);
  isPaginating = signal(false);

  canPaginate = computed(() => this.list().length < this.totalCount() && !this.isPaginating());

  private loadData(paginationParams: IPaginationParams) {
    const isNext = paginationParams.skip > 0;

    this.setLoading(isNext, true);

    this.baseApiService.getList<TEntity[]>(this.url, paginationParams).subscribe({
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
