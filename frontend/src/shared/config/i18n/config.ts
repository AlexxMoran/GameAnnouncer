import { translationEn } from "@shared/config/i18n/en";
import { translationRu } from "@shared/config/i18n/ru";
import i18next from "i18next";
import ICU from "i18next-icu";

export const i18nConfig = {
  resources: {
    en: {
      translation: translationEn,
    },
    ru: {
      translation: translationRu,
    },
  },
  lng: "ru",
  interpolation: {
    escapeValue: false,
  },
};

const i18nextInstance = i18next.createInstance(i18nConfig);
i18nextInstance.use(ICU).init();

export default i18nextInstance;
