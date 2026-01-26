import type { TApiResponseWrapper } from "@shared/services/api/base-api-service/types";
import type {
  IEntityIdField,
  TEntityId,
} from "@shared/types/commonEntity.types";
import type {
  IPaginationMeta,
  IPaginationParams,
} from "@shared/types/pagination.types";
import type { AxiosResponse } from "axios";

export interface IEntityCrudServiceParams<
  TEntity extends IEntityIdField,
  TGetListParams extends IPaginationParams,
  TCreateParams = never,
  TEditParams = never,
> {
  getEntitiesFn: (
    params: TGetListParams,
  ) => Promise<AxiosResponse<TApiResponseWrapper<TEntity[]> & IPaginationMeta>>;
  createEntityFn?: (
    params: TCreateParams,
  ) => Promise<AxiosResponse<TApiResponseWrapper<TEntity>>>;
  editEntityFn?: (
    id: TEntityId,
    params: TEditParams,
  ) => Promise<AxiosResponse<TApiResponseWrapper<TEntity>>>;
  deleteEntityFn?: (
    id: TEntityId,
  ) => Promise<AxiosResponse<TApiResponseWrapper<TEntity>>>;
}
