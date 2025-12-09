import { EGameCategories } from '@shared/api/games/games-api.const';
import { IPaginationParams } from '@shared/lib/pagination/pagination.types';
import { IEntityDateFields } from '@shared/lib/utility-types/base-entity.types';

export interface IGameDto extends IEntityDateFields {
  id: number;
  name: string;
  category: EGameCategories;
  announcements_count: number;
  description?: string;
  image_url?: string;
}

export interface IGetGameListDto extends IPaginationParams {}
