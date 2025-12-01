import { EGameCategories } from '@entities/games/model/game-categories.const';
import { IEntityDateFields } from '@shared/lib/api/base-entity.types';

export interface IGame extends IEntityDateFields {
  id: number;
  name: string;
  category: EGameCategories;
  description?: string;
  image_url?: string;
}
