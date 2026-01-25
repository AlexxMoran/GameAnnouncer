import type { TApiResponseWrapper } from "@shared/services/api/base-api-service/types";
import type { TObjectAny } from "@shared/types/main.types";
import type {
  IPaginationMeta,
  IPaginationParams,
} from "@shared/types/pagination.types";
import type { AxiosResponse } from "axios";

export interface IPaginationServiceParams<
  TEntity extends TObjectAny & { id: TEntityId },
  TParams extends IPaginationParams
> {
  loadFn: (
    params: TParams
  ) => Promise<AxiosResponse<TApiResponseWrapper<TEntity[]> & IPaginationMeta>>;
}

export type TEntityId = number;
