import type {
  IEntityDateFields,
  IEntityIdField,
} from "@shared/types/commonEntity.types";
import type { IPaginationParams } from "@shared/types/pagination.types";

export interface IAnnouncementDto extends IEntityDateFields, IEntityIdField {
  title: string;
  content: string;
  game_id: number;
  image_url: string;
  organizer_id: number;
  status: string;
  start_at: string;
  registration_start_at: string;
  registration_end_at: string;
  max_participants: number;
}

export interface ICreateAnnouncementDto {
  game_id: string;
  title: string;
  content: string;
  start_at: string;
  registration_start_at: string;
  registration_end_at: string;
  max_participants: number;
}

export interface IAnnouncementListFilters {
  game_id?: string;
}

export interface IEditAnnouncementDto
  extends Partial<Omit<ICreateAnnouncementDto, "game_id">> {}

export interface IGetAnnouncementListDto
  extends IPaginationParams,
    IAnnouncementListFilters {}
