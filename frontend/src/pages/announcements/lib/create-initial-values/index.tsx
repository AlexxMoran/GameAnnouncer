import { ERegistrationFormFieldTypes } from "@shared/services/api/announcements-api-service/constants";
import type { IRegistrationFormFieldWithId } from "@shared/services/api/announcements-api-service/types";

export const createInitialValues = (fieldList: IRegistrationFormFieldWithId[]) => {
  return fieldList.reduce<Record<string, string | boolean>>((acc, { id, field_type }) => {
    switch (field_type) {
      case ERegistrationFormFieldTypes.Boolean: {
        acc[id] = false;

        break;
      }

      default: {
        acc[id] = "";
      }
    }

    return acc;
  }, {});
};
