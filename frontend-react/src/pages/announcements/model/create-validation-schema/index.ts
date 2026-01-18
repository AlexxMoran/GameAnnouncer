import type { ICreateAnnouncementsFields } from "@pages/announcements/model/create-validation-schema/types";
import type { TFunction } from "i18next";
import * as Yup from "yup";

export const createValidationSchema = (
  t: TFunction
): Yup.ObjectSchema<ICreateAnnouncementsFields> =>
  Yup.object().shape({
    title: Yup.string()
      .trim()
      .max(64, t("validationErrors.maxLength", { maxLength: 64 }))
      .required(t("validationErrors.required")),
    content: Yup.string()
      .trim()
      .min(8, t("validationErrors.minLength", { minLength: 8 }))
      .max(256, t("validationErrors.maxLength", { maxLength: 256 }))
      .required(t("validationErrors.required")),
    game_id: Yup.string().trim().required(t("validationErrors.required")),
    start_at: Yup.string().trim().required(t("validationErrors.required")),
    registration_start_at: Yup.string()
      .trim()
      .required(t("validationErrors.required")),
    registration_end_at: Yup.string()
      .trim()
      .required(t("validationErrors.required")),
    max_participants: Yup.number()
      .min(2, t("validationErrors", { count: 2 }))
      .required(t("validationErrors.required")),
  });
