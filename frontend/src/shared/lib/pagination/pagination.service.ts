import { computed, signal } from '@angular/core';
import { DEFAULT_LIMIT } from '@shared/lib/pagination/pagination.const';
import { IPaginationConfig } from '@shared/lib/pagination/pagination.types';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { TObjectAny } from '@shared/lib/utility-types/object.types';
import { BehaviorSubject, finalize, map, Observable, scan, switchMap, tap } from 'rxjs';

export class PaginationService<TEntity extends TObjectAny, TFilter extends TObjectAny = {}> {
  private trigger$ = new BehaviorSubject<number>(0);
  private skip = 0;
  private limit = DEFAULT_LIMIT;
  private filters = signal<TFilter>({} as TFilter);
  total = signal<TMaybe<number>>(null);
  isInitializeLoading = signal(false);
  isPaginating = signal(false);
  list$: Observable<TEntity[]>;

  canLoadMore = computed(
    () =>
      !this.isPaginating() &&
      !this.isInitializeLoading() &&
      (this.total() === null || this.limit * (this.skip + 1) < this.total()!),
  );

  constructor(config: IPaginationConfig<TEntity>) {
    if (config.limit) {
      this.limit = config.limit;
    }

    this.list$ = this.trigger$.pipe(
      switchMap((skip) => {
        this.setLoading(true);

        return config.loadDataFn({ skip, limit: this.limit, ...this.filters() }).pipe(
          tap((response) => this.total.set(response.total)),
          map((response) => response.data),
          finalize(() => this.setLoading(false)),
        );
      }),
      scan((acc, newList) => (this.skip === 0 ? newList : acc.concat(newList)), [] as TEntity[]),
    );
  }

  private setLoading(value: boolean) {
    if (this.skip === 0) {
      this.isInitializeLoading.set(value);
    } else {
      this.isPaginating.set(value);
    }
  }

  paginate = () => {
    if (this.canLoadMore()) {
      this.skip += 1;
      this.trigger$.next(this.skip);
    }
  };

  addFilters = (filters: TFilter) => {
    this.filters.set(filters);
    this.reset();
  };

  clearFilters = () => {
    this.filters.set({} as TFilter);
    this.reset();
  };

  reset = () => {
    this.skip = 0;
    this.total.set(null);
    this.trigger$.next(0);
  };
}
