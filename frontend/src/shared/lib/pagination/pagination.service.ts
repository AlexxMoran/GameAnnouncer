import { computed, signal } from '@angular/core';
import { DEFAULT_LIMIT } from '@shared/lib/pagination/pagination.const';
import { IPaginationConfig } from '@shared/lib/pagination/pagination.types';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { TObjectAny } from '@shared/lib/utility-types/object.types';
import {
  BehaviorSubject,
  catchError,
  EMPTY,
  finalize,
  map,
  Observable,
  scan,
  switchMap,
  tap,
} from 'rxjs';

export class PaginationService<TEntity extends TObjectAny, TFilter extends TObjectAny = {}> {
  private trigger$ = new BehaviorSubject<boolean>(false);
  private skip = 0;
  private limit = DEFAULT_LIMIT;
  private filters = signal<TFilter>({} as TFilter);
  hasError = false;
  total = signal<TMaybe<number>>(null);
  isInitializeLoading = signal(false);
  isPaginating = signal(false);
  list$: Observable<TEntity[]>;

  canLoadMore = computed(
    () =>
      !this.isPaginating() &&
      !this.isInitializeLoading() &&
      (this.total() === null || this.skip < this.total()!),
  );

  constructor(config: IPaginationConfig<TEntity>) {
    if (config.limit) {
      this.limit = config.limit;
    }

    this.list$ = this.trigger$.pipe(
      switchMap((next: boolean) => {
        this.setLoading(next, true);

        return config
          .loadDataFn({ skip: next ? this.skip : 0, limit: this.limit, ...this.filters() })
          .pipe(
            tap((response) => this.total.set(response.total)),
            map((response) => response.data),
            catchError(() => {
              if (!next) {
                this.total.set(0);
              }
              // чтобы поток не завершился при ошибке сети
              return EMPTY;
            }),
            finalize(() => this.setLoading(next, false)),
          );
      }),
      scan((acc, newList) => (this.skip === 0 ? newList : acc.concat(newList)), [] as TEntity[]),
      tap({
        next: (list) => (this.skip = list.length),
      }),
    );
  }

  private setLoading(next: boolean, value: boolean) {
    if (next) {
      this.isPaginating.set(value);
    } else {
      this.isInitializeLoading.set(value);
    }
  }

  paginate = () => {
    if (this.canLoadMore()) {
      this.trigger$.next(true);
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
    this.trigger$.next(false);
  };
}
