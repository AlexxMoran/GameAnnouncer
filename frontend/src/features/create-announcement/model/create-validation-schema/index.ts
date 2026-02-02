import type { ICreateAnnouncementsFields } from "@features/create-announcement/model/create-validation-schema/types";
import type { IGameDto } from "@shared/services/api/games-api-service/types";
import dayjs from "dayjs";
import type { TFunction } from "i18next";
import * as Yup from "yup";

export const createValidationSchema = (t: TFunction): Yup.ObjectSchema<ICreateAnnouncementsFields> =>
  Yup.object().shape({
    title: Yup.string()
      .trim()
      .max(64, t("validationErrors.maxLength", { maxLength: 64 }))
      .required(t("validationErrors.required")),
    content: Yup.string()
      .trim()
      .max(256, t("validationErrors.maxLength", { maxLength: 256 })),
    game: Yup.mixed<IGameDto>().required(t("validationErrors.required")),
    start_at: Yup.string()
      .trim()
      .required(t("validationErrors.required"))
      .test("is-valid-date", t("validationErrors.invalidDate"), (value) => {
        if (!value) return false;
        return dayjs(value).isValid();
      }),
    registration_start_at: Yup.string()
      .trim()
      .required(t("validationErrors.required"))
      .test("is-valid-date", t("validationErrors.invalidDate"), (value) => {
        if (!value) return false;
        return dayjs(value).isValid();
      }),
    registration_end_at: Yup.string()
      .trim()
      .required(t("validationErrors.required"))
      .test("is-valid-date", t("validationErrors.invalidDate"), (value) => {
        if (!value) return false;
        return dayjs(value).isValid();
      }),
    max_participants: Yup.number()
      .test("is-valid-min-count", t("validationErrors.minCount", { count: 2 }), (value) => {
        if (!value) return false;
        return value >= 2;
      })
      .test("is-valid-max-count", t("validationErrors.maxCount", { count: 64 }), (value) => {
        if (!value) return false;
        return value <= 64;
      })
      .required(t("validationErrors.required")),
  });
