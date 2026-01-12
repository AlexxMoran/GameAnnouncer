import { computed, signal } from '@angular/core';
import { DEFAULT_LIMIT } from '@shared/lib/list-service/list-service.constants';
import { IPaginationConfig } from '@shared/lib/list-service/list-service.types';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { IEntityIdField } from '@shared/lib/utility-types/base-entity.types';
import { TObjectAny } from '@shared/lib/utility-types/object.types';
import { Subject, takeUntil, tap } from 'rxjs';

export class ListService<TEntity extends IEntityIdField, TFilter extends TObjectAny = {}> {
  readonly list = signal<TEntity[]>([]);
  readonly isInitializeLoading = signal(false);
  readonly isPaginating = signal(false);
  readonly total = signal<TMaybe<number>>(null);
  readonly hasDataToLoad = signal(true);
  readonly filters = signal<TFilter>({} as TFilter);
  readonly hasNoData = computed(() => this.total() === 0);
  private limit = DEFAULT_LIMIT;
  private destroy$ = new Subject<void>();

  constructor(private config: IPaginationConfig<TEntity>) {
    if (config.limit) {
      this.limit = config.limit;
    }
  }

  get paginationParams() {
    return { skip: this.list().length, limit: this.limit, ...this.filters() };
  }

  paginate = () => {
    if (this.isPaginating() || this.isInitializeLoading() || !this.hasDataToLoad()) return;

    this.isPaginating.set(true);

    this.config
      .loadDataFn(this.paginationParams)
      .pipe(
        takeUntil(this.destroy$),
        tap(() => this.isPaginating.set(false)),
      )
      .subscribe((result) => {
        const { data, total } = result;
        const list = this.list();
        const newList = list.concat(data);

        this.hasDataToLoad.set(newList.length < total);
        this.total.set(total);
        this.list.set(newList);
      });
  };

  resetList = () => {
    this.isInitializeLoading.set(false);
    this.isPaginating.set(false);
    this.total.set(null);
    this.list.set([]);
    this.destroy();
    this.init();
  };

  editEntity = (entity: TEntity) => {
    const list = this.list();
    const changedList = list.map((listEntity) =>
      listEntity.id === entity.id ? entity : listEntity,
    );

    this.list.set(changedList);
  };

  addFilters = (filters: TFilter) => {
    this.filters.set(filters);
    this.resetList();
  };

  clearFilters = () => {
    this.filters.set({} as TFilter);
    this.resetList();
  };

  destroy = () => {
    this.destroy$.next();
    this.destroy$.complete();
    this.destroy$ = new Subject();
  };

  init = () => {
    this.isInitializeLoading.set(true);

    this.config
      .loadDataFn(this.paginationParams)
      .pipe(
        takeUntil(this.destroy$),
        tap(() => this.isInitializeLoading.set(false)),
      )
      .subscribe({
        next: (result) => {
          const { data, total } = result;

          this.hasDataToLoad.set(data.length < total);
          this.total.set(total);
          this.list.set(data);
        },
        error: () => {
          this.total.set(0);
        },
      });
  };
}
