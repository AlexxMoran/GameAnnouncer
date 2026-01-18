import type { ICreateAnnouncementsFields } from "@pages/announcements/model/create-validation-schema/types";

export interface ICreateAnnouncementFormProps {
  onSubmit?: (values: ICreateAnnouncementsFields) => Promise<unknown>;
}
