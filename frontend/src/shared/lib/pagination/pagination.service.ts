import { signal } from '@angular/core';
import { DEFAULT_LIMIT } from '@shared/lib/pagination/pagination.const';
import { IPaginationConfig } from '@shared/lib/pagination/pagination.types';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { TObjectAny } from '@shared/lib/utility-types/object.types';
import { BehaviorSubject, finalize, map, Observable, scan, switchMap, takeWhile, tap } from 'rxjs';

export class PaginationService<TEntity extends TObjectAny> {
  private trigger$ = new BehaviorSubject<number>(0);
  private skip = 0;
  total = signal<TMaybe<number>>(null);
  isInitializeLoading = signal(false);
  isPaginating = signal(false);
  list$: Observable<TEntity[]>;

  constructor(config: IPaginationConfig<TEntity>) {
    const limit = config.limit || DEFAULT_LIMIT;

    this.list$ = this.trigger$.pipe(
      takeWhile(() => this.total() === null || limit * this.skip < this.total()!),
      tap(() => this.setLoading(true)),
      switchMap((skip) =>
        config.loadDataFn({ skip, limit }).pipe(
          tap((response) => this.total.set(response.total)),
          map((response) => response.data),
          finalize(() => this.setLoading(false)),
        ),
      ),
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
    if (this.isPaginating() || this.isInitializeLoading()) {
      return;
    }

    this.skip += 1;
    this.trigger$.next(this.skip);
  };

  reset = () => {
    this.skip = 0;
    this.total.set(null);
    this.trigger$.next(0);
  };
}
