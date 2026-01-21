import { IPaginationParams } from '@shared/lib/list-service/list-service.types';
import { IEntityDateFields, IEntityIdField } from '@shared/lib/utility-types/base-entity.types';

export interface IAnnouncementDto extends IEntityDateFields, IEntityIdField {
  title: string;
  content: string;
  game_id: number;
  organizer_id: number;
}

export interface ICreateAnnouncementDto {
  game_id: string;
  title: string;
  content: string;
}

export interface IAnnouncementListFilters {
  game_id?: string;
}

export interface IEditAnnouncementDto extends Partial<Omit<ICreateAnnouncementDto, 'game_id'>> {}

export interface IGetAnnouncementListDto extends IPaginationParams, IAnnouncementListFilters {}
