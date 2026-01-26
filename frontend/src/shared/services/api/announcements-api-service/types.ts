import type { EAnnouncementStatuses } from "@shared/services/api/announcements-api-service/constants";
import type {
  IEntityDateFields,
  IEntityIdField,
} from "@shared/types/commonEntity.types";
import type { TMaybe } from "@shared/types/main.types";
import type { IPaginationParams } from "@shared/types/pagination.types";

export interface IAnnouncementDto extends IEntityDateFields, IEntityIdField {
  title: string;
  content: TMaybe<string>;
  game_id: number;
  image_url: string;
  organizer_id: number;
  status: EAnnouncementStatuses;
  start_at: string;
  end_at: string;
  registration_start_at: string;
  registration_end_at: string;
  max_participants: number;
  participants_count: number;
}

export interface ICreateAnnouncementDto {
  game_id: number;
  title: string;
  content?: string;
  start_at: string;
  registration_start_at: string;
  registration_end_at: string;
  max_participants: number;
}

export interface IAnnouncementListFilters {
  game_id?: string;
  q?: string;
  status?: EAnnouncementStatuses;
}

export interface IEditAnnouncementDto extends Partial<
  Omit<ICreateAnnouncementDto, "game_id">
> {}

export interface IGetAnnouncementsDto
  extends IPaginationParams, IAnnouncementListFilters {}

export interface IGetParticipatedAnnouncementsDto extends IPaginationParams {}
export interface IGetOrganizedAnnouncementsDto extends IPaginationParams {}
