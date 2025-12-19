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
  of,
  scan,
  switchMap,
  tap,
} from 'rxjs';

interface ITriggerParams<TEntity extends TObjectAny> {
  isNext: boolean;
  entityToUpdate?: TEntity;
}

export interface IEntity {
  id: number;
}

export class PaginationService<TEntity extends IEntity, TFilter extends TObjectAny = {}> {
  private trigger$ = new BehaviorSubject<ITriggerParams<TEntity>>({ isNext: true });
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
      (this.total() === null || this.skip < this.total()!),
  );

  constructor(private config: IPaginationConfig<TEntity>) {
    if (config.limit) {
      this.limit = config.limit;
    }

    this.list$ = this.trigger$.pipe(
      switchMap(({ isNext, entityToUpdate }) => {
        if (entityToUpdate) {
          return of({ data: [], isNext, entityToUpdate });
        }

        return this.createLoadingDataStream(isNext);
      }),
      scan((acc, { data, isNext, entityToUpdate }) => {
        if (entityToUpdate) {
          return acc.map((entity) => (entityToUpdate.id === entity.id ? entityToUpdate : entity));
        }

        return isNext ? acc.concat(data) : data;
      }, [] as TEntity[]),
      tap({
        next: (list) => (this.skip = list.length),
      }),
    );
  }

  private createLoadingDataStream = (isNext: boolean, entityToUpdate?: TEntity) => {
    this.setLoading(isNext, true);

    return this.config
      .loadDataFn({ skip: isNext ? this.skip : 0, limit: this.limit, ...this.filters() })
      .pipe(
        tap((response) => this.total.set(response.total)),
        map((response) => ({ ...response, isNext, entityToUpdate })),
        catchError(() => {
          if (!isNext) {
            this.total.set(0);
          }
          // чтобы поток не завершился при ошибке сети
          return EMPTY;
        }),
        finalize(() => this.setLoading(isNext, false)),
      );
  };

  private setLoading(next: boolean, value: boolean) {
    if (next) {
      this.isPaginating.set(value);
    } else {
      this.isInitializeLoading.set(value);
    }
  }

  paginate = () => {
    if (this.canLoadMore()) {
      this.trigger$.next({ isNext: true });
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

  editEntity = (entity: TEntity) => {
    this.trigger$.next({ isNext: false, entityToUpdate: entity });
  };

  reset = () => {
    this.skip = 0;
    this.total.set(null);
    this.trigger$.next({ isNext: false });
  };
}
