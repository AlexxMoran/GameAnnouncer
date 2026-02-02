import { EGameCategories } from "@shared/services/api/games-api-service/constants";
import type { IEntityDateFields, IEntityIdField } from "@shared/types/commonEntity.types";
import type { IPaginationParams } from "@shared/types/pagination.types";

export interface IGameDto extends IEntityDateFields, IEntityIdField {
  name: string;
  category: EGameCategories;
  announcements_count: number;
  description: string;
  image_url?: string;
}

export interface ICreateGameDto {
  name: string;
  description: string;
  category: EGameCategories;
}

export interface IEditGameDto extends Partial<ICreateGameDto> {}

export interface IGamesFilters {
  name?: string;
}

export interface IGetGamesDto extends IPaginationParams, Partial<IGamesFilters> {}
