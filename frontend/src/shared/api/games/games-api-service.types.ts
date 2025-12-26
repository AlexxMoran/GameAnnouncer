import { EGameCategories } from '@shared/api/games/games-api.constants';
import { IPaginationParams } from '@shared/lib/pagination/pagination.types';
import { IEntityDateFields, IEntityIdField } from '@shared/lib/utility-types/base-entity.types';

export interface IGameDto extends IEntityDateFields, IEntityIdField {
  name: string;
  category: EGameCategories;
  announcements_count: number;
  description?: string;
  image_url?: string;
}

export interface ICreateGameDto {
  name: string;
  description: string;
  category: EGameCategories;
}

export interface IEditGameDto extends Partial<ICreateGameDto> {}

export interface IGameListFilters {
  category: EGameCategories;
}

export interface IGetGameListDto extends IPaginationParams, Partial<IGameListFilters> {}
