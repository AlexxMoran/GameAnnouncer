import { TApiResponseWrapper } from '@shared/api/base-api-service.types';
import { TObjectAny } from '@shared/lib/utility-types/object.types';
import { Observable } from 'rxjs';

export interface IPaginationParams {
  skip: number;
  limit: number;
}

export interface IPaginationMeta {
  total: number;
}

export type TLoadDataFn<TEntity extends TObjectAny> = (
  params?: TObjectAny & IPaginationParams,
) => Observable<TApiResponseWrapper<TEntity[]> & IPaginationMeta>;

export interface IPaginationConfig<TEntity extends TObjectAny> {
  loadDataFn: TLoadDataFn<TEntity>;
  limit?: number;
}

export interface ITriggerParams<TEntity extends TObjectAny> {
  isNext: boolean;
  entityToUpdate?: TEntity;
}
