import {
  ICreateAnnouncementDto,
  IEditAnnouncementDto,
} from '@shared/api/announcements/announcements-api-service.types';

export interface ICreateAnnouncementParams extends ICreateAnnouncementDto {}
export interface IEditAnnouncementParams extends IEditAnnouncementDto {}
