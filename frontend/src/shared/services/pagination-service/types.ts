import type { TApiResponseWrapper } from "@shared/services/api/base-api-service/types";
import type { IEntityIdField } from "@shared/types/commonEntity.types";
import type { IPaginationMeta, IPaginationParams } from "@shared/types/pagination.types";
import type { AxiosResponse } from "axios";

export interface IPaginationServiceParams<TEntity extends IEntityIdField, TParams extends IPaginationParams> {
  loadFn: (params: TParams) => Promise<AxiosResponse<TApiResponseWrapper<TEntity[]> & IPaginationMeta>>;
  initImmediately?: boolean;
}
